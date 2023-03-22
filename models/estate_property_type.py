
from odoo import fields, models

class Estate_Property_Type(models.Model):
    _name = 'estate.property.type'
    _description = "State type property"

    active = fields.Boolean(default=True)

    name = fields.Char(required=True)
