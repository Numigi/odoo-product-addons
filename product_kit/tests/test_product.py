# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.tests import common
from odoo.exceptions import ValidationError


class TestProduct(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uom_dozen = cls.env.ref("uom.product_uom_dozen")
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_day = cls.env.ref("uom.product_uom_day")
        cls.component = cls.env["product.product"].create(
            {"name": "My Component", "type": "consu", "uom_id": cls.uom_unit.id}
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "My Kit",
                "is_kit": True,
                "type": "service",
                "kit_line_ids": [
                    (
                        0,
                        0,
                        {"component_id": cls.component.id, "uom_id": cls.uom_dozen.id},
                    )
                ],
            }
        )

    def test_kit_must_be_a_service(self):
        with pytest.raises(ValidationError):
            self.product.type = "consu"

    def test_component_uom_category(self):
        with pytest.raises(ValidationError):
            self.component.write(
                {"uom_id": self.uom_day.id, "uom_po_id": self.uom_day.id}
            )
