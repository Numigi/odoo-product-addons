# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product State Extended",
    "version": "14.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://numigi.com/r/home",
    "license": "AGPL-3",
    "category": "Product",
    "depends": [
        "product_state",
        "product_pack",
        "sale_rental",
        "purchase",
        "hr_expense",
    ],
    "summary": """
        This module allows you to manage product states effectively.
    """,
    "data": [
        "security/product_security.xml",
        "security/ir.model.access.csv",
        "data/product_state_data.xml",
        "views/product_template.xml",
    ],
    "post_init_hook": "_update_data_translation",
    "installable": True,
}
