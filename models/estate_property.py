from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import fields, models


class Lead(models.Model):
    STATES_CHOICES = [
        ('New', 'New'),
        ('Offer Received', 'Offer Received'),
        ('Offer Accepted', 'Offer Accepted'),
        ('Sold', 'Sold'),
        ('Canceled', 'Canceled'),
    ]

    _name = 'estate.model'
    _description = "State property"

    active = fields.Boolean(default=True)

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: (datetime.now() + relativedelta(months=3)))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer(default=3)
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

    state = fields.Selection(
        string='State',
        default=STATES_CHOICES[0][0],
        selection=STATES_CHOICES
    )
