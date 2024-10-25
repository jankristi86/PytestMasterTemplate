import os
import logging as logger
from config.hosts_config import WOO_API_HOSTS
from utilities.credentials_utility import CredentialsUtility
from woocommerce import API


class WooAPIUtility(object):

    # because of ORDERS API won't work with oath request-utility,
    # using instead the official woocommerce api for request utility

    def __init__(self):
        self.rs_json = None
        self.expected_status_code = None
        self.status_code = None
        self.url = None
        wc_creds = CredentialsUtility.get_wc_api_keys()
        self.env = os.environ.get('ENV', 'test')
        self.base_url = WOO_API_HOSTS[self.env]
        self.wcapi = API(
            url=self.base_url,
            consumer_key=wc_creds['wc_key'],
            consumer_secret=wc_creds['wc_secret'],
            version="wc/v3"
        )

    def assert_status_code(self):
        assert self.status_code == self.expected_status_code, f"Bad status code." \
                                                              f"Expected {self.expected_status_code}, Actual status " \
                                                              f"code: {self.status_code}," \
                                                              f"URL: {self.url}, Response JSON: {self.rs_json}"

    def get(self, wc_endpoint, params=None, expected_status_code=200):
        rs_api = self.wcapi.get(wc_endpoint, params=params)

        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.assert_status_code()

        logger.debug(f"API GET response: {self.rs_json}")

        return self.rs_json

    def post(self, wc_endpoint, params=None, expected_status_code=200):
        rs_api = self.wcapi.post(wc_endpoint, data=params)

        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.assert_status_code()

        logger.debug(f"API POST response: {self.rs_json}")

        return self.rs_json

    def put(self, wc_endpoint, params=None, expected_status_code=200):
        rs_api = self.wcapi.put(wc_endpoint, data=params)

        self.status_code = rs_api.status_code
        self.expected_status_code = expected_status_code
        self.rs_json = rs_api.json()
        self.assert_status_code()

        logger.debug(f"API PUT response: {self.rs_json}")

        return self.rs_json


if __name__ == '__main__':
    obj = WooAPIUtility()
    rs_api = obj.get('products')
    print(rs_api)
