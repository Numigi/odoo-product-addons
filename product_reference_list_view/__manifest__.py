# -*- coding: utf-8 -*-
# © 2020 - Today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

{
    'name': 'Product Reference List View',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'AGPL-3',
    'category': 'Product',
    'summary': 'Add a list view to load and consult product references.',
    'depends': [
        'product_reference',
        'product_panel_shortcut',
    ],
    'data': [
        'views/product_template_reference.xml',
    ],
    'installable': True,
}
