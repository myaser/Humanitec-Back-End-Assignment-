import requests
from flask import current_app

from app.exceptions import IntegrityError
from app.gateways import AbstractJSONStorageGateway, get_default_gateway


class OrderRepository(object):

    @staticmethod
    def create(data, gateway: AbstractJSONStorageGateway = None):
        gateway = gateway if gateway is not None else get_default_gateway()
        response = requests.get(f"{current_app.config['PRODUCTS_SERVICE_URL']}/{data['product_uuid']}/")
        if response.ok:
            return gateway.create(data)
        else:
            raise IntegrityError('product not found')

    @staticmethod
    def retrieve(uuid, gateway: AbstractJSONStorageGateway = None):
        gateway = gateway if gateway is not None else get_default_gateway()
        return gateway.retrieve(uuid)

    @staticmethod
    def update(uuid, data, gateway: AbstractJSONStorageGateway = None):
        # ignore other parameters in payload
        gateway = gateway if gateway is not None else get_default_gateway()
        return gateway.update(uuid=uuid, data={'quantity': data.pop('quantity')})

    @staticmethod
    def delete(uuid, gateway: AbstractJSONStorageGateway = None):
        gateway = gateway if gateway is not None else get_default_gateway()
        return gateway.delete(uuid=uuid)

    @staticmethod
    def list_(gateway: AbstractJSONStorageGateway = None):
        gateway = gateway if gateway is not None else get_default_gateway()
        return gateway.list_()
