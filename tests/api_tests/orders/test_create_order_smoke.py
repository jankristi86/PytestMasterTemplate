import pytest
from dao.products_dao import ProductsDAO
from helpers.orders_helper import OrdersHelper
from helpers.customers_helper import CustomerHelper

pytestmark = [pytest.mark.orders, pytest.mark.smoke, pytest.mark.api_tests]

""" 
    with my_orders_setup method avoiding repetitive get_random_product for each case.
    scope fixture will execute only once on module level (for all tests),
    without module decorator, it will execute each time and provide different ids
    also creating object of helper and dao classes on setup level can save memory for
    creating object in each test, instead I am returning objects as a dict on fixture setup level
    and passing it within test  
"""


@pytest.fixture(scope='module')
def my_orders_setup():
    product_dao = ProductsDAO()
    orders_helper = OrdersHelper()
    customer_helper = CustomerHelper()
    rand_product = product_dao.get_random_product_from_db(1)
    product_id = rand_product[0]['ID']

    # pass as a dictionary
    info = {'product_id': product_id,
            'orders_helper': orders_helper,
            'customer_helper': customer_helper}
    return info


@pytest.mark.tcid48
def test_create_paid_order_guest_user(my_orders_setup):
    orders_helper = my_orders_setup['orders_helper']
    customer_id = 0
    product_id = my_orders_setup['product_id']

    # make the call
    info = {"line_items": [
        {
            "product_id": product_id,
            "quantity": 2
        }
    ]}
    order_json = orders_helper.create_order(additional_args=info)

    # verify response
    expected_products = [{'product_id': product_id}]
    orders_helper.verify_order_is_created(order_json=order_json, exp_customer_id=customer_id,
                                          expected_products=expected_products)


@pytest.mark.tcid49
def test_create_paid_order_new_created_customer(my_orders_setup):
    orders_helper = my_orders_setup['orders_helper']
    customer_helper = my_orders_setup['customer_helper']
    product_id = my_orders_setup['product_id']

    # make the call
    cust_info = customer_helper.create_customer()
    customer_id = cust_info['id']

    info = {"line_items": [
        {
            "product_id": product_id,
            "quantity": 2
        }
    ],
        "customer_id": customer_id}
    order_json = orders_helper.create_order(additional_args=info)

    # verify response
    expected_products = [{'product_id': product_id}]
    orders_helper.verify_order_is_created(order_json=order_json, exp_customer_id=customer_id,
                                          expected_products=expected_products)
