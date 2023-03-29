
from odoo import fields, models

class Estate_Property_Type(models.Model):
    _name = 'estate.property.type'
    _description = "State type property"
    _order = "name"

    active = fields.Boolean(default=True)

    name = fields.Char(required=True)

    property_ids = fields.One2many("estate.model", "property_type_id", string="Estate property")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    # property_type_id = fields.Many2one("estate.property.offer", string="Offer")
    # description = fields.Char(related="property_type_id.partner_id", store=True)

    vehicle_count = fields.Integer(compute='compute_count')

    def compute_count(self):
        for record in self:
            record.vehicle_count = self.env['estate.property.offer'].search_count(
                [('property_type_id', '=', self.id)])

    def get_vehicles(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Offers',
            'view_mode': 'tree',
            'res_model': 'estate.property.offer',
            'domain': [('property_type_id', '=', self.id)],
            'context': "{'create': False}"
        }


    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',  'You can not have two type properties with the same name !')
    ]
