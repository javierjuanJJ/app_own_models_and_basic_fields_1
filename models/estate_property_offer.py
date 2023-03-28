from odoo import fields, models, api

from dateutil.relativedelta import relativedelta

from odoo.exceptions import UserError

STATES_OFFER_CHOICES = [
    ('Accepted', 'Accepted'),
    ('Refused', 'Refused')
]

class Estate_Property_Offer(models.Model):



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

    date_deadline = fields.Date(compute="_compute_total", inverse='_inverse_total', store=True)
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

    def action_accept(self):
        for record in self:
            if not record.state == STATES_OFFER_CHOICES[0][0]:

                if not len(record.property_id.offer_ids.filtered(lambda r: r.state == "Accepted")) == 0:
                    raise UserError('The properties can not be sold by more than 1 person')

                record.property_id.selling_price = self.price
                record.property_id.buyer_id = self.partner_id.id

            record.state = STATES_OFFER_CHOICES[0][0]

        return True

    def action_reffuse(self):
        for record in self:
            record.state = STATES_OFFER_CHOICES[1][0]
        return True

    _sql_constraints = [
        ('price_check', 'CHECK(price >= 0)', 'The price must be a strictly positive number.')
    ]