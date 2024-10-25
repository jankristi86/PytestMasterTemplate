from tests.ui_tests.tc import TC


class BasePage(object):
    def __init__(self, tc):
        self.tc = tc  # type: TC
        self.driver = tc.driver
        from view_objects import views
        self.views = views
