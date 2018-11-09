import ujson as json
from unittest.mock import patch
from uuid import UUID

import responses

from app.exceptions import NoResultFound
from app.repositories import ProductRepository
from app.tests.base import BaseTestCase


class TestAPI(BaseTestCase):

    def test_create_product(self):
        payload = {
            'name': 'test product',
            'price': 150.5
        }
        response = self.client.post(
            '/products/',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
            data=json.dumps(payload)
        )
        self.assertStatus(response, 201)

    @patch('app.gateways.uuid4', new=lambda: UUID('2ec2757a-5651-47af-977b-7e3e91e1888f'))
    def test_create_product_duplicate_key(self):
        payload = {
            'name': 'test product',
            'price': 150.5
        }
        response = self.client.post(
            '/products/',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
            data=json.dumps(payload)
        )
        self.assertStatus(response, 201)

        payload = {
            'name': 'test product',
            'price': 150.5
        }
        response = self.client.post(
            '/products/',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
            data=json.dumps(payload)
        )
        self.assertStatus(response, 500)

    def test_update_product(self):
        # create product
        product = ProductRepository.create({'price': 1.5, 'name': 'sample 1'})
        product_uuid = product['uuid']
        # update price
        response = self.client.patch(
            f'/products/{product_uuid}',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
            data=json.dumps({'price': 2})
        )
        self.assert_status(response, 204)
        self.assertEquals(ProductRepository.retrieve(product["uuid"])['price'], '2')

        # update product_uuid
        response = self.client.patch(
            f'/products/{product_uuid}',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
            data=json.dumps({'uuid': '42f616dd-ea9f-41c0-a4d2-389be68b2a99'})
        )
        self.assert_status(response, 204)
        self.assertEquals(ProductRepository.retrieve(product["uuid"])['price'], '2')

        # update name and price
        response = self.client.patch(
            f'/products/{product_uuid}',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
            data=json.dumps(
                {
                    'uuid': '42f616dd-ea9f-41c0-a4d2-389be68b2a99',
                    'price': 3,
                    'name': 'sample 2',
                }
            )
        )
        self.assert_status(response, 204)
        product = ProductRepository.list_()[0]
        self.assertEquals(product['price'], '3')
        self.assertEquals(product['uuid'], product_uuid)
        self.assertEquals(product['name'], 'sample 2')

        # update product not found
        response = self.client.patch(
            f'/products/42f616dd-ea9f-41c0-a4d2-389be68b2a99',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
            data=json.dumps({'price': 2})
        )
        self.assert_status(response, 404)

    def test_get_product(self):
        product = ProductRepository.create({'price': 1.5, 'name': 'sample 1'})

        response = self.client.get(
            '/products/uuid_not_found',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
        )
        self.assert404(response)

        response = self.client.get(
            f'/products/{product["uuid"]}',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
        )
        self.assert200(response)

    def test_list_products(self):
        ProductRepository.create({'price': 1.5, 'name': 'sample 1'})
        ProductRepository.create({'price': 2.5, 'name': 'sample 2'})

        response = self.client.get(
            '/products/',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
        )
        self.assertStatus(response, 200)
        self.assertTrue(response.is_json)
        self.assertEqual(len(response.get_json()), 2)

    @responses.activate
    def test_delete_product_not_booked(self):
        product = ProductRepository.create({'price': 1.5, 'name': 'sample 1'})
        responses.add(responses.GET, self.app.config['ORDERS_SERVICE_URL'] + f'/?product_uuid={product["uuid"]}',
                      status=404)

        # delete product
        response = self.client.delete(
            f'/products/{product["uuid"]}',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
        )
        self.assert_status(response, 204)

        with self.assertRaises(NoResultFound):
            ProductRepository.retrieve(product['uuid'])

        # delete product not found
        response = self.client.delete(
            f'/products/{product["uuid"]}',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
        )
        self.assert_status(response, 404)

    @responses.activate
    def test_delete_product_booked(self):
        product = ProductRepository.create({'price': 1.5, 'name': 'sample 1'})
        responses.add(responses.GET, self.app.config['ORDERS_SERVICE_URL'] + f'/?product_uuid={product["uuid"]}',
                      status=200)

        # delete product
        response = self.client.delete(
            f'/products/{product["uuid"]}',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
        )
        self.assert_status(response, 409)

        ProductRepository.retrieve(product['uuid'])
