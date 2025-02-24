# This file is part purchase_create_shipment module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool

from .purchase import Configuration, ConfigurationPurchaseMethod, Purchase


def register():
    Pool.register(
        Configuration,
        ConfigurationPurchaseMethod,
        Purchase,
        module='purchase_create_shipment', type_='model')
