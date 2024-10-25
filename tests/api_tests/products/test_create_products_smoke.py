import pytest
from utilities.generic_utilities import generate_random_string

from tests.api_tests.base_test import BaseTest

pytestmark = [pytest.mark.products, pytest.mark.smoke]

"""
On this sub-suite inherited base_test class with its setup's and teardown's,
also using test context class having instantiated objects for each util, helper
class needed for those particular tests. This way avoiding creating instance
of those classes on every single test."""


@pytest.mark.api_tests
class TestCreateProducts(BaseTest):

    @pytest.mark.tcid26
    def test_create_one_simple_product(self):
        # test data
        name = generate_random_string(20)
        _type = "simple"
        regular_price = "10.99"

        # # make the call
        product_rs = self.tc.products_payload_helper.create_simple_product(name, _type, regular_price)

        # validate the response
        assert product_rs, f"Create product api response is empty. Product name: {name}"
        assert product_rs['name'] == name, f"Create product api call response has unexpected name." \
                                           f"Expected: {name}, Actual: {product_rs['name']}"
        # validate the product exists in db
        product_id = product_rs['id']
        db_product = self.tc.products_dao.get_product_by_id(product_id)
        assert name == db_product[0]['post_title'], f"Create product title in db does not match title in api." \
                                                    f"DB: {db_product['post_title']}, API request: {name}"
