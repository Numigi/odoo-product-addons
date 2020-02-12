FROM quay.io/numigi/odoo-public:12.latest
MAINTAINER numigi <contact@numigi.com>

USER root

COPY .docker_files/test-requirements.txt .
RUN pip3 install -r test-requirements.txt

# Variable used for fetching private git repositories.
ARG GIT_TOKEN

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"
COPY ./gitoo.yml /gitoo.yml
RUN gitoo install-all --conf_file /gitoo.yml --destination "${THIRD_PARTY_ADDONS}"

USER odoo

COPY product_create_group /mnt/extra-addons/product_create_group
COPY product_extra_views /mnt/extra-addons/product_extra_views
COPY product_extra_views_purchase /mnt/extra-addons/product_extra_views_purchase
COPY product_extra_views_sale /mnt/extra-addons/product_extra_views_sale
COPY product_extra_views_stock /mnt/extra-addons/product_extra_views_stock
COPY product_dimension /mnt/extra-addons/product_dimension
COPY product_reference /mnt/extra-addons/product_reference
COPY product_supplier_name_search /mnt/extra-addons/product_supplier_name_search

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
