# © 2017 Savoir-faire Linux
# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Product Dimensions',
    'version': "14.0.1.0.0",
    'author': 'Savoir-faire Linux',
    'maintainer': 'Numigi',
    'website': 'https://numigi.com/r/home',
    'license': 'LGPL-3',
    'category': 'Product',
    'summary': 'Add extra measure fields to products.',
    'depends': ['stock'],
    'data': [
        'data/decimal_precision.xml',
        'views/float_with_uom.xml',
        'views/product.xml',
        'views/product_template.xml',
    ],
    'installable': True,
}
