from odoo import fields, models

class Lead(models.Model):
    _name = "estate.property"
    _description = "State property"

    name= fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientations',
        selection=[
            ('North', 'north'),
            ('East', 'east'),
            ('South', 'south'),
            ('West', 'west')
        ]
    )