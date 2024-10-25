import pytest

from tests.api_tests.base_test import BaseTest


@pytest.mark.api_tests
class TestGetCustomers(BaseTest):

    @pytest.mark.customers
    @pytest.mark.tcid30
    def test_get_all_customer(self):
        # make the call
        rs_api = self.tc.requests_utility.get('customers')

        # validate response
        assert rs_api, f"Response of list all customers is empty."
