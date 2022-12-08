# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Product Create Group',
    'version': "14.0.1.0.0",
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Partner Management',
    'summary': 'Add a group to create/edit products and variants',
    'depends': [
        'product',
        'base_extended_security',
    ],
    'data': [
        'security/res_groups.xml',
        'security/extended_security_rule.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
