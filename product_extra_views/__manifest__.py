# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Product Extra Views',
    'version': "14.0.1.0.0",
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://numigi.com/r/home',
    'license': 'LGPL-3',
    'category': 'Product',
    'summary': 'Add pivot and graph views to products',
    'depends': [
        'product',
    ],
    'data': [
        'views/product_template.xml',
        'views/product_product.xml',
    ],
    'installable': True,
}
