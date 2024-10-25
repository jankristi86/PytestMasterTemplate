import os
import json
from utilities.woo_requests_utility import WooAPIUtility
from dao.orders_dao import OrdersDAO


class OrdersHelper(object):

    def __init__(self):
        self.cur_file_dir = os.path.dirname(os.path.realpath(__file__))
        self.woo_helper = WooAPIUtility()

    def create_order(self, additional_args=None):
        payload_template = os.path.join(self.cur_file_dir, '..', 'data',
                                        'payload_json_data', 'create_order_payload.json')

        with open(payload_template) as f:
            payload = json.load(f)
        # if user add more info to payload, then update it
        if additional_args:
            assert isinstance(additional_args, dict), f"Parameter 'additional args' must be a dictionary but found" \
                                                      f"{type(additional_args)}"
            payload.update(additional_args)
        rs_api = self.woo_helper.post('orders', params=payload, expected_status_code=201)

        return rs_api

    @staticmethod
    def verify_order_is_created(order_json, exp_customer_id, expected_products):
        orders_dao = OrdersDAO()

        # verify response
        assert order_json, f"Create order response is empty."
        assert order_json['customer_id'] == exp_customer_id, f"Create order with given customer id returned bad" \
                                                             f"customer id. Expected customer_id = {exp_customer_id}, " \
                                                             f"but got '{order_json['customer_id']}'"
        assert len(order_json['line_items']) == len(
            expected_products), f"Expected only {len(expected_products)} item in order," \
                                f"but found '{len(order_json['line_items'])}'" \
                                f"Order id: {order_json['id']}."
        # verify db
        order_id = order_json['id']
        line_info = orders_dao.get_order_lines_by_order_id(order_id)
        assert line_info, f"Create order, line item not found in DB. Order id: {order_id}"

        line_items = [i for i in line_info if i['order_item_type'] == 'line_item']

        assert len(line_items) == 1, f"Expected 1 line item, but found {len(line_items)}. Order id: {order_id}"

        # get list of product ids in the response
        api_product_ids = [i['product_id'] for i in order_json['line_items']]
        for product in expected_products:
            assert product[
                       'product_id'] in api_product_ids, f"Create order does not have at least 1 expected product in DB." \
                                                         f"Product id: {product['product_id']}, Order id: {order_id}"

    def call_update_an_order(self, order_id, payload):
        return self.woo_helper.put(f"orders/{order_id}", params=payload)

    def call_retrieve_an_order(self, order_id):
        return self.woo_helper.get(f"orders/{order_id}")
