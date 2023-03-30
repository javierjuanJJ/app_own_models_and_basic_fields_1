from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare

GARDEN_ORIENTATION_CHOICES = [
    ('North', 'north'),
    ('East', 'east'),
    ('South', 'south'),
    ('West', 'west')
]

STATES_CHOICES = [
    ('New', 'New'),
    ('Offer Received', 'Offer Received'),
    ('Offer Accepted', 'Offer Accepted'),
    ('Sold', 'Sold'),
    ('Canceled', 'Canceled'),
]

STATES_OFFER_CHOICES = [
    ('Accepted', 'Accepted'),
    ('Refused', 'Refused')
]


class Lead(models.Model):

    _name = 'estate.model'
    # _inherit = 'res.partner'
    _description = "State property"
    _order = "id desc"

    active = fields.Boolean(default=True)

    name = fields.Char(required=True)
    create_date = fields.Date('Create Date', readonly=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: (datetime.now() + relativedelta(months=3)))
    expected_price = fields.Float(required=True)
    # selling_price = fields.Float(compute="check_change_selling_price",readonly=False)
    selling_price = fields.Float(readonly=False)
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
    tag_ids = fields.Many2many("estate.property.tag", string="Tags", options="{'color_field': 'color'}")

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

    def cancel_button(self):
        for record in self:
            if record.state == STATES_CHOICES[3][0]:
                raise UserError(
                    'You can not cancel a solded property'
                )
            record.state = STATES_CHOICES[4][0]
        return True

    def sold_button(self):
        for record in self:
            if record.state == STATES_CHOICES[4][0]:
                raise UserError(
                    'You can not sell a cancelled property'
                )
            record.state = STATES_CHOICES[3][0]
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_if_user_inactive(self):
        if not (self.state == 'New' or self.state == 'Canceled'):
            raise UserError("Can't delete an new or canceled property!")

    _sql_constraints = [
        ('expected_price_check', 'CHECK(expected_price > 0)', 'The expected price must be a strictly positive number.'),
        ('selling_price_check', 'CHECK(selling_price >= 0)', 'The selling price must be a positive number.')
    ]

    # @api.depends('selling_price')
    # def check_change_selling_price(self):
    #     self.check_quantity()

    @api.constrains('selling_price')
    def check_quantity(self):
        for quant in self:
            expected_price_to_compare = self.expected_price * 0.9
            if float_compare(self.selling_price, (expected_price_to_compare), precision_digits=2) < 0:
                raise ValidationError(f'The selling price value must be greater than {(expected_price_to_compare)} because is 90% of {self.expected_price}')


    # def update_seller(self, seller, price):
    #     print('not record.state == STATES_OFFER_CHOICES[0][0]:')
    #     self.salesperson_id = seller
    #     self.selling_price = price


