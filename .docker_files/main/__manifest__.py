# © 2018 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Main Module',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Install all addons required for testing.',
    'depends': [
        'product_extra_views',
        'product_extra_views_purchase',
        'product_extra_views_sale',
        'product_extra_views_stock',
        'product_reference',
        'product_dimension',
        'product_supplier_name_search',
        'stock_inventory_category_domain',
    ],
    'installable': True,
}
