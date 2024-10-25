import copy

from data.payload_dict_data.products_payload import SIMPLE_PRODUCT_PAYLOAD
from utilities.requests_utility import RequestsUtility
import logging as logger


class ProductsHelper(object):

    def __init__(self):
        self.request_utility = RequestsUtility()

    def get_product_by_id(self, product_id):
        return self.request_utility.get(f"products/{product_id}")

    def call_create_product(self, payload):
        return self.request_utility.post('products', payload=payload, expected_status_code=201)

    def call_update_a_product(self, product_id, payload):
        return self.request_utility.put(f"products/{product_id}", payload=payload)

    def call_list_products(self, payload=None):

        max_pages = 1000
        all_products = []
        for i in range(1, max_pages + 1):
            logger.debug(f"List products page number: {i}")
            if 'per_page' not in payload.keys():
                payload['per_page'] = 100

            # add current page  number to the call
            payload['page'] = i
            rs_api = self.request_utility.get('products', payload=payload)

            # if there is no response stop the loop, cause there are no products
            if not rs_api:
                break
            else:
                all_products.extend(rs_api)
        else:
            raise Exception(f"Unable to find all products after {max_pages} pages.")

        return all_products


class ProductsPayloadHelper(object):

    @staticmethod
    def create_simple_product(name, _type, regular_price, **kwargs):
        payload = copy.deepcopy(SIMPLE_PRODUCT_PAYLOAD)
        pmod = payload
        if name:
            pmod['name'] = name
        if _type:
            pmod['type'] = _type
        if regular_price:
            pmod['regular_price'] = regular_price
        product_rs = ProductsHelper().call_create_product(payload=payload)
        return product_rs
