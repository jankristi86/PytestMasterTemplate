import time

from selenium.webdriver.common.by import By

from data.constants import Uri
from element_objects.element import Element
from tests.ui_tests.tc import TC
from view_objects.base_page import BasePage


class LoginView(BasePage):
    def __init__(self, tc):
        super(LoginView, self).__init__(tc=tc)
        self.tc = tc  # type: TC
        self.driver = tc.driver

        self.ID_USERNAME = 'username'
        self.ID_PASSWORD = 'password'
        self.XP_BTN_SUBMIT = '//button[@name="login"]'
        self.XP_LOGIN_VALIDATION = '//div[@class="woocommerce-MyAccount-content"]/p[contains(text(),"Hello")]'
        self.username = Element(page=self, locator=self.ID_USERNAME, select_by=By.ID)
        self.password = Element(page=self, locator=self.ID_PASSWORD, select_by=By.ID)
        self.btn_submit = Element(page=self, locator=self.XP_BTN_SUBMIT)
        self.login_validation = Element(page=self, locator=self.XP_LOGIN_VALIDATION)

    def input_username(self, username):
        self.username.send_keys(username)

    def input_password(self, password):
        self.password.send_keys(password)

    def click_login(self):
        self.btn_submit.wait_until_clickable().click()
        time.sleep(2)
        assert self.driver.current_url.endswith(Uri.MY_ACCOUNT.value)

    def get_login_validation_msg(self):
        return self.login_validation.get_text()
