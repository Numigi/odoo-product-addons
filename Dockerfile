FROM quay.io/numigi/odoo-public:11.0
MAINTAINER numigi <contact@numigi.com>

COPY product_dimension /mnt/extra-addons/product_dimension
COPY product_reference /mnt/extra-addons/product_reference
COPY product_supplier_name_search /mnt/extra-addons/product_supplier_name_search

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
