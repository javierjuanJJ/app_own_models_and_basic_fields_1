from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api

GARDEN_ORIENTATION_CHOICES = [
    ('North', 'north'),
    ('East', 'east'),
    ('South', 'south'),
    ('West', 'west')
]


class Lead(models.Model):
    STATES_CHOICES = [
        ('New', 'New'),
        ('Offer Received', 'Offer Received'),
        ('Offer Accepted', 'Offer Accepted'),
        ('Sold', 'Sold'),
        ('Canceled', 'Canceled'),
    ]

    _name = 'estate.model'
    # _inherit = 'res.partner'
    _description = "State property"

    active = fields.Boolean(default=True)

    name = fields.Char(required=True)
    create_date = fields.Date('Create Date', readonly=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: (datetime.now() + relativedelta(months=3)))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer(default=3)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientations',
        selection=GARDEN_ORIENTATION_CHOICES
    )

    state = fields.Selection(
        string='State',
        default=STATES_CHOICES[0][0],
        selection=STATES_CHOICES
    )

    property_type_id = fields.Many2one("estate.property.type", string="Name")

    salesperson_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True,
                                     default=lambda self: self.env.user)

    buyer_id = fields.Many2one('res.partner', string='Buyer', index=True, default=lambda self: self.env.company.id)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Estate property offer")
    total_area = fields.Float(compute="_compute_total", store=True)
    best_price = fields.Float(compute="_highest_price_order", store=True)

    @api.depends('offer_ids.price')
    def _highest_price_order(self):
        for record in self:
            total = max(record.offer_ids.mapped('price')) if record.offer_ids else 0
            record.best_price = total

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange("garden")
    def _onchange_partner_id(self):

        if self.garden_orientation == None:
            return {'warning': {
                'title': "Warning",
                'message': ('The garden have not choice orientation')}}

        if self.garden:
            self.garden_area = 10
            self.garden_orientation = GARDEN_ORIENTATION_CHOICES[0][0]
        else:
            self.garden_area = 0
            self.garden_orientation = None
