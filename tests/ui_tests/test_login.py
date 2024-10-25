import pytest

from tests.ui_tests.base_test import BaseTest
from view_objects import views


@pytest.mark.ui_tests
class TestLogin(BaseTest):

    @pytest.mark.tcid1
    def test_1(self):
        dash_view = views.DashboardView(self.tc)
        dash_view.get_dropdown(name='orderby').value = 'Sort by latest'
        dash_view.get_nav_menu('nav-menu').value = 'My account'
        login_view = views.LoginView(self.tc)
        login_view.input_username('admin')
        login_view.input_password('admin')
        login_view.click_login()
        assert login_view.get_login_validation_msg()
        assert 'admin' in login_view.get_login_validation_msg()
