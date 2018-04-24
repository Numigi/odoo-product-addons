/*
    © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("product_dimension.float_with_uom", function(require) {
    "use strict";

    var registry = require("web.field_registry");

    var FloatWithUoM = registry.get("float").extend({
        /**
         * Setup the related uom field attribute.
         */
        init() {
            this._super.apply(this, arguments);
            this._uomField = this.attrs.uom_field;
            if(!this._uomField){
                console.log(
                    "Missing attribute uom_field on the field " +
                    this.name + " of model " + this.model + ".");
            }
        },
        /**
         * Add the unit of measure to the value to display in the field in readonly mode.
         */
        _formatValue(){
            var number = this._super.apply(this, arguments);
            if(this.mode === "readonly"){
                var uom = this._getUoMDisplayValue();
                return number && uom ? number + " " + uom : number;
            }
            return number;
        },
        /**
         * Get the name of the unit of measure related to the field.
         */
        _getUoMDisplayValue(){
            if(!this._uomField){
                return null;
            }
            var uom = this.record.data[this._uomField];
            return uom ? uom.data.display_name : null;
        },
    });

    registry.add("float_with_uom", FloatWithUoM);
});
