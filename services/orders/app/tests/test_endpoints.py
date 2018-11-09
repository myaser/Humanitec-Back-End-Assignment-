import ujson as json
from unittest.mock import patch
from uuid import UUID

import responses

from app.exceptions import NoResultFound
from app.repositories import OrderRepository
from app.tests.base import BaseTestCase


class TestAPI(BaseTestCase):

    @responses.activate
    def test_create_order_with_product_that_exists(self):
        responses.add(responses.GET, self.app.config['PRODUCTS_SERVICE_URL'] + '/415781d4-b14f-4995-85cb-b681571801c2/',
                      json={'uuid': '415781d4-b14f-4995-85cb-b681571801c2', 'name': 'existing_product', 'price': 10},
                      status=200)

        payload = {'quantity': 1,
                   'product_uuid': '415781d4-b14f-4995-85cb-b681571801c2'}
        response = self.client.post(
            '/orders/',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
            data=json.dumps(payload)
        )
        self.assertStatus(response, 201)

    @patch('app.gateways.uuid4', new=lambda: UUID('2ec2757a-5651-47af-977b-7e3e91e1888f'))
    @responses.activate
    def test_create_order_with_product_that_exists_duplicate_key(self):
        responses.add(responses.GET, self.app.config['PRODUCTS_SERVICE_URL'] + '/415781d4-b14f-4995-85cb-b681571801c2/',
                      json={'uuid': '415781d4-b14f-4995-85cb-b681571801c2', 'name': 'existing_product', 'price': 10},
                      status=200)

        payload = {'quantity': 1,
                   'product_uuid': '415781d4-b14f-4995-85cb-b681571801c2'}
        response = self.client.post(
            '/orders/',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
            data=json.dumps(payload)
        )
        self.assertStatus(response, 201)

        response = self.client.post(
            '/orders/',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
            data=json.dumps(payload)
        )
        self.assertStatus(response, 500)

    @responses.activate
    def test_create_order_with_product_that_does_not_exist(self):
        responses.add(responses.GET, self.app.config['PRODUCTS_SERVICE_URL'] + '/415781d4-b14f-4995-85cb-b681571801c2/',
                      json={"message": "product not found"},
                      status=404)

        payload = {'quantity': 1,
                   'product_uuid': '415781d4-b14f-4995-85cb-b681571801c2'}
        response = self.client.post(
            '/orders/',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
            data=json.dumps(payload)
        )
        self.assertStatus(response, 409)

    @responses.activate
    def test_get_list(self):
        responses.add(responses.GET, self.app.config['PRODUCTS_SERVICE_URL'] + '/415781d4-b14f-4995-85cb-b681571801c2/',
                      json={'uuid': '415781d4-b14f-4995-85cb-b681571801c2', 'name': 'existing_product', 'price': 10},
                      status=200)
        OrderRepository.create({'quantity': '1', 'product_uuid': '415781d4-b14f-4995-85cb-b681571801c2'})
        OrderRepository.create({'quantity': '1', 'product_uuid': '415781d4-b14f-4995-85cb-b681571801c2'})

        response = self.client.get(
            '/orders/',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
        )
        self.assertStatus(response, 200)
        self.assertTrue(response.is_json)
        self.assertEqual(len(response.get_json()), 2)

    @responses.activate
    def test_get_item(self):
        responses.add(responses.GET, self.app.config['PRODUCTS_SERVICE_URL'] + '/415781d4-b14f-4995-85cb-b681571801c2/',
                      json={'uuid': '415781d4-b14f-4995-85cb-b681571801c2', 'name': 'existing_product', 'price': 10},
                      status=200)
        order = OrderRepository.create({'quantity': '1', 'product_uuid': '415781d4-b14f-4995-85cb-b681571801c2'})

        response = self.client.get(
            '/orders/uuid_not_found',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
        )
        self.assert404(response)

        response = self.client.get(
            f'/orders/{order["uuid"]}',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
        )
        self.assert200(response)

    @responses.activate
    def test_update_item(self):
        responses.add(responses.GET, self.app.config['PRODUCTS_SERVICE_URL'] + '/415781d4-b14f-4995-85cb-b681571801c2/',
                      json={'uuid': '415781d4-b14f-4995-85cb-b681571801c2', 'name': 'existing_product', 'price': 10},
                      status=200)
        # create order
        order = OrderRepository.create({'quantity': '1', 'product_uuid': '415781d4-b14f-4995-85cb-b681571801c2'})

        # update quantity
        response = self.client.patch(
            f'/orders/{order["uuid"]}',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
            data=json.dumps({'quantity': 2})
        )
        self.assert_status(response, 204)

        self.assertEquals(OrderRepository.retrieve(order["uuid"])['quantity'], 2)

        # update product_uuid
        response = self.client.patch(
            f'/orders/{order["uuid"]}',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
            data=json.dumps({'product_uuid': '42f616dd-ea9f-41c0-a4d2-389be68b2a99'})
        )
        self.assert400(response)

        # update quantity and product_uuid
        response = self.client.patch(
            f'/orders/{order["uuid"]}',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
            data=json.dumps(
                {
                    'product_uuid': '42f616dd-ea9f-41c0-a4d2-389be68b2a99',
                    'quantity': 3
                }
            )
        )
        self.assert_status(response, 204)
        order = OrderRepository.retrieve(order["uuid"])
        self.assertEquals(order['quantity'], 3)
        self.assertEquals(order['product_uuid'], '415781d4-b14f-4995-85cb-b681571801c2')

        # update order not found
        response = self.client.patch(
            f'/orders/42f616dd-ea9f-41c0-a4d2-389be68b2a99',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
            data=json.dumps({'quantity': 2})
        )
        self.assert_status(response, 404)

        # test update order uuid
        response = self.client.patch(
            f'/orders/{order["uuid"]}',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
            data=json.dumps({'uuid': '42f616dd-ea9f-41c0-a4d2-389be68b2a99', 'quantity': 100})
        )
        self.assert_status(response, 204)
        self.assertEqual(OrderRepository.retrieve(order["uuid"])['quantity'], 100)
        with self.assertRaises(NoResultFound):
            OrderRepository.retrieve("42f616dd-ea9f-41c0-a4d2-389be68b2a99")

    @responses.activate
    def test_delete_item(self):
        responses.add(responses.GET, self.app.config['PRODUCTS_SERVICE_URL'] + '/415781d4-b14f-4995-85cb-b681571801c2/',
                      json={'uuid': '415781d4-b14f-4995-85cb-b681571801c2', 'name': 'existing_product', 'price': 10},
                      status=200)
        # create order
        order = OrderRepository.create({'quantity': '1', 'product_uuid': '415781d4-b14f-4995-85cb-b681571801c2'})

        # delete order
        response = self.client.delete(
            f'/orders/{order["uuid"]}',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
        )
        self.assert_status(response, 204)
        with self.assertRaises(NoResultFound):
            OrderRepository.retrieve(order['uuid'])

        # delete order not found
        response = self.client.delete(
            f'/orders/42f616dd-ea9f-41c0-a4d2-389be68b2a99',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
        )
        self.assert_status(response, 404)

    @responses.activate
    def test_search_by_product_uuid(self):
        responses.add(responses.GET, self.app.config['PRODUCTS_SERVICE_URL'] + '/415781d4-b14f-4995-85cb-b681571801c2/',
                      json={'uuid': '415781d4-b14f-4995-85cb-b681571801c2', 'name': 'existing_product', 'price': 10},
                      status=200)
        OrderRepository.create({'quantity': '1', 'product_uuid': '415781d4-b14f-4995-85cb-b681571801c2'})
        response = self.client.get(
            '/orders/?product_uuid=415781d4-b14f-4995-85cb-b681571801c2',
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.test_jwt_token}'},
        )
        self.assertStatus(response, 200)
        self.assertTrue(response.is_json)
        self.assertEqual(len(response.get_json()), 1)
        self.assertEqual(response.get_json()[0]['product_uuid'], '415781d4-b14f-4995-85cb-b681571801c2')
