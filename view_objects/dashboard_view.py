from tests.ui_tests.tc import TC
from view_objects.base_page import BasePage
from element_objects.element import DropdownElement, NavMenuSelector

from selenium.webdriver.common.by import By


class DashboardView(BasePage):
    def __init__(self, tc):
        super(DashboardView, self).__init__(tc=tc)
        self.tc = tc  # type: TC
        self.driver = tc.driver

    def get_dropdown(self, name):
        locator = f"//select[@name='{name}']"
        return DropdownElement(page=self, locator=locator)

    def get_nav_menu(self, name):
        locator = f"//div[@class='menu']//ul[@class='{name}']"
        return NavMenuSelector(page=self, locator=locator)
