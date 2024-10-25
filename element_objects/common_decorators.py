import os.path
import time

from selenium.common import TimeoutException, StaleElementReferenceException
from configobj import ConfigObj

DEFAULT_TIMEOUT_MID = 10
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\data'))
MAIN_CONFIG = ConfigObj(os.path.join(BASE_PATH, 'main.cfg'))


def retry(retriable_exceptions, max_retries=3, delay=0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    if i < max_retries - 1:
                        retriable = False
                        for exception in retriable_exceptions:
                            if isinstance(ex, exception):
                                retriable = True
                                break

                        if retriable:
                            if delay > 0:
                                time.sleep(delay)

                            continue
                    raise ex

        return wrapper

    return decorator


def timeout_retry(max_retries=3):
    return retry([TimeoutException], max_retries)


def stale_retry(max_retries=int(MAIN_CONFIG['Constants']['retry_limit'])):
    return retry([StaleElementReferenceException], max_retries)
