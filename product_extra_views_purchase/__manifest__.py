# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Product Extra Views / Purchase',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://bit.ly/numigi-com',
    'license': 'LGPL-3',
    'category': 'Product',
    'summary': 'Add pivot and graph views to products from purchases',
    'depends': [
        'product_extra_views',
        'purchase',
    ],
    'data': [
        'views/menu.xml',
    ],
    'installable': True,
    'auto_install': True,
}
