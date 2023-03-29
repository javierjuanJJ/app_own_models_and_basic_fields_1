
from odoo import fields, models

class Estate_Property_Type(models.Model):
    _name = 'estate.property.type'
    _description = "State type property"
    _order = "name"

    active = fields.Boolean(default=True)

    name = fields.Char(required=True)

    property_ids = fields.One2many("estate.model", "property_type_id", string="Estate property")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',  'You can not have two type properties with the same name !')
    ]
