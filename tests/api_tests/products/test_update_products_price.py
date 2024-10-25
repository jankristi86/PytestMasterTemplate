import copy
import pytest
import random
from utilities.generic_utilities import generate_random_string
from data.payload_dict_data import products_payload
from tests.api_tests.base_test import BaseTest

pytestmark = [pytest.mark.products, pytest.mark.regression]

"""
On this sub-suite inherited base_test class with its setup's and teardown's,
also using test context class having instantiated objects for each util, helper
class needed for those particular tests. This way avoiding creating instance
of those classes on every single test."""


@pytest.mark.api_tests
class TestProductsUpdatePrice(BaseTest):

    @pytest.mark.tcid61
    def test_verify_update_new_product_regular_price(self):
        # test data
        new_price = '15.00'
        name = generate_random_string(20)
        _type = "simple"
        regular_price = "10.99"

        # call create a product
        product_rs = self.tc.products_payload_helper.create_simple_product(name, _type, regular_price)

        # validate product created with the payload provided price
        assert regular_price == product_rs['regular_price'], \
            f"Product: {product_rs['id']} was not created with the price: {regular_price}" \
            f"Actual price: {product_rs['regular_price']}"

        # providing update product price data
        payload = copy.deepcopy(products_payload.UPDATE_PRODUCT_PRICE_PAYLOAD)
        pmod = payload
        pmod['regular_price'] = new_price

        # call update product price
        put_res = self.tc.products_helper.call_update_a_product(product_rs['id'], payload=payload)

        # validate product is updated with the new price
        get_resp = self.tc.products_helper.get_product_by_id(put_res['id'])
        assert get_resp['regular_price'] == put_res['regular_price'], \
            f"Product price was not updated correctly for the product id: {product_rs['id']}. " \
            f"Expected: {new_price}, actual: {get_resp['regular_price']}"

    @pytest.mark.tcid611
    def test_update_regular_price_existing_product_should_update_price(self):
        """
        Verifies updating the 'regular_price' field should automatically update the 'price' field.
        """

        # create helper objects and get random product from db
        # product_helper = ProductsHelper()
        # product_dao = ProductsDAO()

        # for this test the 'sale_price' of the product must be empty. If product has sale price, updating the 'regular_price'
        # does not update the 'price'. So get a bunch of products and loop untill you find one that is not on sale. If all in
        # the list are on sale then take random one and update the sale price
        rand_products = self.tc.products_dao.get_random_product_from_db(30)
        for product in rand_products:
            product_id = product['ID']
            product_data = self.tc.products_helper.get_product_by_id(product_id)
            if product_data['on_sale']:
                continue
            else:
                break
        else:
            # take a random product and make it not on sale by setting sale_price=''
            test_product = random.choice(rand_products)
            product_id = test_product['ID']
            self.tc.products_helper.call_update_a_product(product_id, {'sale_price': ''})

        # make the update to 'regular_price'
        new_price = str(random.randint(10, 100)) + '.' + str(random.randint(10, 99))
        payload = dict()
        payload['regular_price'] = new_price

        rs_update = self.tc.products_helper.call_update_a_product(product_id, payload=payload)

        # verify the response has the 'price' and 'regular_price' has updated and 'sale_price' is not updated
        assert rs_update[
                   'price'] == new_price, f"Update product api call response. Updating the 'regular_price' did not " \
                                          f"update the 'price' field. price field actual value {rs_update['price']}," \
                                          f"but expected: {new_price}"

        assert rs_update['regular_price'] == new_price, \
            f"Update product api call response. Updating the 'regular_price' did not " \
            f"update in the response. Actual response 'regular_price'={rs_update['price']}," \
            f"but expected: {new_price}"

        # get the product after the update and verify response
        rs_product = self.tc.products_helper.get_product_by_id(product_id)
        assert rs_product[
                   'price'] == new_price, f"Update product api call response. Updating the 'regular_price' did not " \
                                          f"update the 'price' field. price field actual value {rs_product['price']}," \
                                          f"but expected: {new_price}"

        assert rs_product['regular_price'] == new_price, \
            f"Update product api call response. Updating the 'regular_price' did not " \
            f"update. Actual 'regular_price'={rs_product['price']}," \
            f"but expected: {new_price}"

    @pytest.mark.tcid63
    @pytest.mark.tcid64
    def test_validate_on_sale_true_when_updated_sale_price(self):
        # data
        self.product_id = None
        regular_price = str(random.randint(10, 100)) + '.' + str(random.randint(10, 99))
        name = generate_random_string(20)
        _type = "simple"

        # get random product not on_sale, if not in DB, generate a simple one
        products = self.tc.products_dao.get_random_product_from_db(30)
        for product in products:
            self.product_id = product['ID']
            product_data = self.tc.products_helper.get_product_by_id(self.product_id)
            if product_data['on_sale']:
                # and not product_data['regular_price']
                continue
            else:
                break
        else:
            product = self.tc.products_payload_helper.create_simple_product(name, _type, regular_price)
            self.product_id = product['id']

        # get product
        product_id = self.product_id
        regular_price = self.tc.products_helper.get_product_by_id(product_id)

        # tcid63 update 'sale_price' and verify the 'on_sale' is set to True
        sale_price = float(regular_price['regular_price']) * 0.75
        payload = dict()
        payload['sale_price'] = str(sale_price)
        request = self.tc.products_helper.call_update_a_product(product_id, payload)
        assert request['price'] == payload['sale_price'], f"Expected for the product: {product_id} " \
                                                          f"price to be updated to: {payload['sale_price']}, " \
                                                          f"but actually price is: {request['price']}"
        assert request['on_sale'], f" Expected on_sale to be set to True, " \
                                   f" Actually it is: {request['on_sale']}"

        # tcid64 verify update the sale_price to empty string and verify the 'on_sale is set to False
        self.tc.products_helper.call_update_a_product(product_id, {'sale_price': ''})
        product_after_update = self.tc.products_helper.get_product_by_id(product_id)
        assert not product_after_update['on_sale'], f"Updated sale_price: '', but the on_sale did not set to False." \
                                                    f"Actually it is: {product_after_update['on_sale']} " \
                                                    f"for the product: {product_id}"

