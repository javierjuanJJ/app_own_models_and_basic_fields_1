from odoo import fields, models, api

from dateutil.relativedelta import relativedelta
class Estate_Property_Offer(models.Model):

    STATES_OFFER_CHOICES = [
        ('Accepted', 'Accepted'),
        ('Refused', 'Refused')
    ]

    _name = 'estate.property.offer'
    _description = "State offer property"

    active = fields.Boolean(default=True)

    price = fields.Float()

    state = fields.Selection(
        string='State',
        default=STATES_OFFER_CHOICES[0][0],
        selection=STATES_OFFER_CHOICES,
        copy=False
    )

    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.model", string="State property", required=True)

    date_deadline = fields.Date(compute="_compute_total", inverse='_inverse_total')
    validity = fields.Integer(default=7)

    @api.depends("create_date", "validity")
    def _compute_total(self):
        for record in self:

            if record.create_date:
                # date = datetime.now()
                date = record.create_date
            else:
                date = fields.Datetime.now()

            new_date = date + relativedelta(days=record.validity)
            # new_date = date + relativedelta(days=record.validity)

            record.date_deadline = new_date

    def _inverse_total(self):
        for record in self:
            new_date = record.date_deadline - relativedelta(days=record.validity)
            # new_date = date + relativedelta(days=record.validity)

            record.create_date = new_date