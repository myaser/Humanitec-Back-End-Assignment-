import requests
from flask import current_app

from app.exceptions import IntegrityError
from app.gateways import AbstractJSONStorageGateway, get_default_gateway


class ProductRepository(object):

    @staticmethod
    def create(data, gateway: AbstractJSONStorageGateway = None):
        gateway = gateway if gateway is not None else get_default_gateway()
        return gateway.create(data)

    @staticmethod
    def retrieve(uuid, gateway: AbstractJSONStorageGateway = None):
        gateway = gateway if gateway is not None else get_default_gateway()
        return gateway.retrieve(uuid)

    @staticmethod
    def update(uuid, data, gateway: AbstractJSONStorageGateway = None):
        gateway = gateway if gateway is not None else get_default_gateway()
        return gateway.update(uuid=uuid, data=data)

    @staticmethod
    def delete(uuid, gateway: AbstractJSONStorageGateway = None):
        gateway = gateway if gateway is not None else get_default_gateway()
        response = requests.get(f"{current_app.config['ORDERS_SERVICE_URL']}/?product_uuid={uuid}")
        if response.ok:
            raise IntegrityError('product is booked in order')
        else:
            return gateway.delete(uuid)

    @staticmethod
    def list_(gateway: AbstractJSONStorageGateway = None):
        gateway = gateway if gateway is not None else get_default_gateway()
        return gateway.list_()
