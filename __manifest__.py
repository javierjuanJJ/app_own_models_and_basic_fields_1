# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Real estate properties',
    'version': '0.1',
    'category': '',
    'sequence': 15,
    'summary': 'Real estate properties',
    'description': "Real estate properties",
    'website': '',
    'depends': [],
    'data': [
        #'models/estate_property.py'
        'security/ir.model.access.csv',
        'views/estate_property.xml',
    ],
    'demo': [],
    'css': [''],
    'installable': True,
    'application': True,
    'auto_install': True
}