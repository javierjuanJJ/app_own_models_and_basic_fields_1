from odoo import fields, models
class Estate_Property_Type(models.Model):
    _name = 'estate.property.tag'
    _description = "State tag property"

    active = fields.Boolean(default=True)

    name = fields.Char(required=True)