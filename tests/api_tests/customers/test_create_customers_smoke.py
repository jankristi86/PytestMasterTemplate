import pytest
import logging as logger
from utilities.generic_utilities import generate_random_email_and_password

from tests.api_tests.base_test import BaseTest

@pytest.mark.api_tests
class TestCreateCustomers(BaseTest):

    @pytest.mark.customers
    @pytest.mark.tcid29
    def test_create_customer_only_email_password(self):
        logger.info('TEST: Create new customer with email and username only')

        rand_info = generate_random_email_and_password()
        email = rand_info['email']
        password = rand_info['password']

        # make the call
        cust_api_info = self.tc.customer_helper.create_customer(email=email, password=password)

        # verify email and first_name in the response
        assert cust_api_info['email'] == email, f"Create customer api return wrong email. Email: {email}"
        assert cust_api_info['first_name'] == '', f"Create customer api returned value for first_name" \
                                                  f"but it should be empty."

        # verify customer is created in db
        cust_info = self.tc.customers_dao.get_customer_by_email(email)

        id_in_api = cust_api_info['id']
        id_in_db = cust_info[0]["ID"]
        assert id_in_api == id_in_db, f'Create customer response "id" not same as "ID" in database.' \
                                      f'Email: {email}'

    @pytest.mark.customers
    @pytest.mark.tcid47
    def test_create_customer_fail_for_existing_email(self):
        # get existing email form db
        existing_cust = self.tc.customers_dao.get_random_customer_from_db()
        existing_email = existing_cust[0]['user_email']

        # call API
        payload = {"email": existing_email, "password": "Password1"}
        cust_api_info = self.tc.requests_utility.post(endpoint="customers", payload=payload, expected_status_code=400)

        # validate response error message
        assert cust_api_info[
                   'code'] == 'registration-error-email-exists', f"Created customer with existing email error " \
                                                                 f"'code' is not correct. " \
                                                                 f"Expected 'registration-error-email-exists', " \
                                                                 f"Actual {cust_api_info['code']}"
