import pytest

from tests.api_tests.base_test import BaseTest

pytestmark = [pytest.mark.products, pytest.mark.smoke]

"""
On this sub-suite inherited base_test class with its setup's and teardown's,
also using test context class having instantiated objects for each util, helper
class needed for those particular tests. This way avoiding creating instance
of those classes on every single test."""


@pytest.mark.api_tests
class TestGetProducts(BaseTest):
    @pytest.mark.tcid24
    def test_get_all_products(self):
        rs_api = self.tc.requests_utility.get('products')
        assert rs_api, f"Response of list all products is empty."

    @pytest.mark.tcid25
    def test_get_product_by_id(self):
        # get a product (test data) from db
        rand_product = self.tc.products_dao.get_random_product_from_db(1)
        rand_product_id = rand_product[0]['ID']
        db_name = rand_product[0]['post_title']

        # make the call
        rs_api = self.tc.products_helper.get_product_by_id(rand_product_id)
        api_name = rs_api['name']

        # verify response
        assert db_name == api_name, f"Get product by id returned wrong product. ID: {rand_product_id}" \
                                    f"DB name: {db_name}, API name: {api_name}"
