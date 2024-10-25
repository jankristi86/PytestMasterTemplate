import pytest
from datetime import datetime, timedelta
from tests.api_tests.base_test import BaseTest

"""
On this sub-suite inherited base_test class with its setup's and teardown's,
also using test context class having instantiated objects for each util, helper
class needed for those particular tests. This way avoiding creating instance
of those classes on every single test."""


@pytest.mark.regression
@pytest.mark.api_tests
class TestListProductsWithFilter(BaseTest):

    @pytest.mark.tcid51
    def test_list_products_with_filter_after(self):
        # create data
        x_days_from_today = 300
        _after_created_date = datetime.now().replace(microsecond=0) - timedelta(days=x_days_from_today)
        after_created_date = _after_created_date.isoformat()
        # other way of dealing with date format
        # tmp_date = datetime.now() - timedelta(days=x_days_from_today)
        # after_created_date = tmp_date.strftime('%Y-%M-%dT%H:%m:%s')

        # make the call
        payload = dict()
        payload['after'] = after_created_date
        rs_api = self.tc.products_helper.call_list_products(payload)
        assert rs_api, f"Empty response for list products with filter"

        # get data from db
        db_products = self.tc.products_dao.get_products_after_given_date(given_date=after_created_date)

        # verify response matches db
        assert len(rs_api) == len(db_products), f"List products with filter 'after', returned unexpected numbers of " \
                                                f"products." \
                                                f"Expected: {len(db_products)}, Actual: {len(rs_api)}"
        ids_in_api = [i['id'] for i in rs_api]
        ids_in_db = [i['ID'] for i in db_products]
        ids_diff = list(set(ids_in_api) - set(ids_in_db))
        assert not ids_diff, f"list products with filter. Products ids in response missmatch in db."
