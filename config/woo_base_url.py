import os
from abc import abstractmethod
import time

from selenium.webdriver.support.wait import WebDriverWait


class WooBaseUrl:
    DEFAULT_TIMEOUT_LONG = 10
    DEFAULT_TIMEOUT_MID = 5
    DEFAULT_TIMEOUT_SHORT = 2
    tab_handles = {}

    def __init__(self, driver, url=""):
        self.url = url
        browser_param = os.getenv('BROWSER_TO_RUN', 'chrome')
        if browser_param == 'chrome':
            driver.get(url)
            self.driver = driver
            time.sleep(self.DEFAULT_TIMEOUT_SHORT)
        else:
            self.driver = driver
            self.open_new_or_existing_tab_then_goto_url(driver)

    @abstractmethod
    def _verify_page(self):
        pass

    def close_web(self):
        self.driver.close()

    def refresh(self):
        self.driver.refresh()

    def open_new_or_existing_tab_then_goto_url(self, driver):
        current_tabs = driver.window_handles
        vals = list(self.tab_handles.values())
        try:
            idx = vals.index(self.url)
            tab = list(self.tab_handles.keys())[idx]
        except ValueError:
            tab = None
        opened_tab = driver.current_window_handle
        if not tab:
            if len(current_tabs) <= 1 and opened_tab not in self.tab_handles:
                self.open_url()
                self.tab_handles[opened_tab] = self.url
                return opened_tab
            else:
                driver.execute_script("window.open('');")
                WebDriverWait(driver, self.DEFAULT_TIMEOUT_LONG).until(
                    lambda _: len(driver.window_handles) > len(current_tabs))
                assert len(driver.window_handles) > len(current_tabs), "Cannot open new tab"
                curr_tabs_with_new_tab = driver.window_handles
                new_tabs = list(set(curr_tabs_with_new_tab) - set(current_tabs))
                driver.switch_to.window(new_tabs[0])
                self.tab_handles[new_tabs[0]] = self.url
                self.open_url()
                return new_tabs[0]
        else:
            if tab == opened_tab:
                self.open_url()
                return tab
            else:
                found_tab = [t for t in current_tabs if t == tab]
                if found_tab:
                    driver.switch_to.window(found_tab[0])
                    self.open_url()
                    return found_tab
                else:
                    assert False, f"Tab {WooBaseUrl.tab} not found in [{current_tabs}]"

    def open_url(self):
        print(f"CURRENT URL: [{self.driver.current_url}]")
        if self.driver.current_url != self.url:
            print(f"Opening Expected url [{self.url}]")
            self.driver.get(self.url)
