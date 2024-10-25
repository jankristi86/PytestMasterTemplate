import unittest

from config import driver_setup, config_logging
from config.config_util import ConfigUtil
from config.woo_base_url import WooBaseUrl
from data.constants import Wait
from tests.ui_tests.tc import TC
from view_objects import views

log = config_logging.config_root(__name__)


class BaseTest(unittest.TestCase):
    tc = None
    driver = None
    restart_count = 0

    @classmethod
    def setUpClass(cls):
        print('BEFORE SUITE')
        cls.driver = driver_setup.get_driver()
        cls.driver.set_window_size(1920, 1080)
        cls.tc = TC(cls.driver)
        cls.base_url = ConfigUtil.get_app_url()
        cls.base_page = WooBaseUrl(cls.driver, cls.base_url)
        cls.landing_page = views.DashboardView(cls.tc)

    def setUp(self):
        print('BEFORE TEST')
        try:
            self.landing_page.my_account_menu.wait_until_visible(Wait.LONG_WAIT)
        except:
            if self.restart_count < 3:
                self.driver.quit()
                self.setUpClass()
                self.restart_count += 1
        log.info("=============")
        log.info(f"= START TEST [{self._testMethodName}]")
        # assert chain

    def tearDown(self):
        print('AFTER TEST')
        log.info("=============")
        log.info(f"= END TEST [{self._testMethodName}]")
        # end assert chain

    @classmethod
    def tearDownClass(cls):
        print('AFTER SUITE')
        cls.driver.quit()


