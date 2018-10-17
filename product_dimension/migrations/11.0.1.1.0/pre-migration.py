# © 2017 Savoir-faire Linux
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    """Delete views that depend on the field weight_uom_id.

    Because weight_uom_id was renamed to specific_weight_uom_id,
    we need to delete all views that depend on it.

    Otherwise, the upgrade of the module fails.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    views_to_update = [
        'product_template_form_view_with_weight_in_uom',
        'product_form_view_with_dimension_label',
    ]

    def delete_view_recursively(view):
        for child in view.inherit_children_ids:
            delete_view_recursively(child)
        view.unlink()

    for view_ref in views_to_update:
        view = env.ref(
            'product_dimension.{ref}'.format(ref=view_ref),
            raise_if_not_found=False)
        if view:
            delete_view_recursively(view)
