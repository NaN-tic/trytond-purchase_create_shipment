from trytond.model import fields
from trytond.pool import Pool, PoolMeta

create_shipment_on_confirm = fields.Boolean("Create Shipment on Confirm")


class Configuration(metaclass=PoolMeta):
    __name__ = 'purchase.configuration'

    create_shipment_on_confirm = fields.MultiValue(create_shipment_on_confirm)

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field == 'create_shipment_on_confirm':
            return pool.get('purchase.configuration.purchase_method')
        return super(Configuration, cls).multivalue_model(field)

    @classmethod
    def default_create_shipment_on_confirm(cls, **pattern):
        return cls.multivalue_model(
            'purchase_invoice_method').default_purchase_invoice_method()


class ConfigurationPurchaseMethod(metaclass=PoolMeta):
    __name__ = 'purchase.configuration.purchase_method'

    create_shipment_on_confirm = create_shipment_on_confirm

    @classmethod
    def default_create_shipment_on_confirm(cls):
        return False


class Purchase(metaclass=PoolMeta):
    __name__ = 'purchase.purchase'

    def create_move(self, move_type):
        Configuration = Pool().get('purchase.configuration')

        moves = super(Purchase, self).create_move(move_type)
        if not Configuration(1).create_shipment_on_confirm:
            return moves

        shipment = None
        if move_type == 'in':
            shipment = self._get_shipment()
        else:
            shipment = self._get_return_shipment()

        shipment.moves = moves
        shipment.save()
        return moves
