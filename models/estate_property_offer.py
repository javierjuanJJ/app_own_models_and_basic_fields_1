from odoo import fields, models
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