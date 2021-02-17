# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Product Dangerous Goods',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'AGPL-3',
    'category': 'Product',
    'summary': 'Add Dangerous option field on product',
    'depends': [
        # Odoo
        "product",
    ],
    'data': [
        # Views
        "views/product_template.xml",
    ],
    'installable': True,
}
