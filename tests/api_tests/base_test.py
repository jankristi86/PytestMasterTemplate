import pytest

from tests.api_tests.tc import TC


class BaseTest:
    tc = TC()

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self):
        pass

    def teardown_method(self):
        pass
