from dao.customers_dao import CustomersDAO
from dao.products_dao import ProductsDAO
from helpers.customers_helper import CustomerHelper
from helpers.products_helper import ProductsHelper, ProductsPayloadHelper
from utilities.requests_utility import RequestsUtility


class TC:

    def __init__(self):
        self.products_helper = ProductsHelper()
        self.products_dao = ProductsDAO()
        self.products_payload_helper = ProductsPayloadHelper()
        self.requests_utility = RequestsUtility()
        self.customer_helper = CustomerHelper()
        self.customers_dao = CustomersDAO()
