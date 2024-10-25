from helpers.orders_helper import OrdersHelper
from utilities.generic_utilities import generate_random_string
from utilities.woo_requests_utility import WooAPIUtility
import pytest

"""
On this sub-suite implementing parametrize decorator
in order to avoid redundant code, given that it is various status check
that is being validated"""

pytestmark = [pytest.mark.orders, pytest.mark.regression, pytest.mark.api_tests]


@pytest.mark.parametrize("new_status", [
    pytest.param('cancelled', marks=[pytest.mark.tcid55, pytest.mark.smoke]),
    pytest.param('completed', marks=pytest.mark.tcid56),
    pytest.param('on-hold', marks=pytest.mark.tcid57),
])
def test_update_order_status(new_status):
    # create new order
    order_helper = OrdersHelper()
    order_json = order_helper.create_order()
    cur_status = order_json['status']
    assert cur_status != new_status, f"Current status order is already '{new_status}'." \
                                     f"Unable to perform the test."

    # update the status
    order_id = order_json['id']
    payload = {"status": new_status}
    order_helper.call_update_an_order(order_id, payload)

    # get order info
    new_order_info = order_helper.call_retrieve_an_order(order_id)

    # validate new order status is updated
    assert new_order_info['status'] == new_status, f"Updated order status to '{new_status}'," \
                                                   f"but order is still '{new_order_info['status']}'"


@pytest.mark.tcid58
def test_update_order_status_to_random_string():
    new_status = generate_random_string(6)

    order_helper = OrdersHelper()
    order_json = order_helper.create_order()

    # update the status
    order_id = order_json['id']
    payload = {"status": new_status}
    res_api = WooAPIUtility().put(f"orders/{order_id}", params=payload, expected_status_code=400)

    assert res_api['code'] == 'rest_invalid_param', \
        f"Update order status to random string did not have," \
        "correct code in response. Expected, rest_invalid_param," \
        f"Actual: '{res_api['code']}'"

    assert res_api['message'] == 'Invalid parameter(s): status', \
        f"Update order status to random string did not have," \
        "correct message in response. Expected, " \
        "rest_invalid_param," \
        f"Actual: '{res_api['message']}'"


@pytest.mark.tcid59
def test_update_order_customer_note():

    order_helper = OrdersHelper()
    order_json = order_helper.create_order()
    order_id = order_json['id']

    customer_note = generate_random_string(20)
    payload = {"customer_note": customer_note}
    order_helper.call_update_an_order(order_id, payload)

    # get order info
    new_order_info = order_helper.call_retrieve_an_order(order_id)

    assert new_order_info['customer_note'] == customer_note, \
        f"Update orders 'customer_note' field failed." \
        f"Expected: {customer_note}, but actual: {new_order_info['customer_note']}"
