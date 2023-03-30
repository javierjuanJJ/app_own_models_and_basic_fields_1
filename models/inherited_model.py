from odoo import fields, models, api

class User(models.Model):

    # _name = 'inherit.users'
    _description = "State offer property"
    _inherit = 'res.users'

    property_ids = fields.One2many("estate.model", "property_id", string="Estate property")



