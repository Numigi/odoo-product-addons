# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Product Template Tag Stock Menu',
    'version': '11.0.1.0.0',
    'author': 'Numigi',
    'maintainer': 'numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Stock',
    'summary': 'Add menu inventory app for product template tags.',
    'depends': [
        'stock',
        'product_template_tags',
    ],
    'data': [
        'views/menu.xml',
    ],
    'installable': True,
    'auto_install': True,
}
