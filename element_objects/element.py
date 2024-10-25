import time
import logging
from selenium.common import InvalidSelectorException, NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from data import constants as const
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from element_objects.common_decorators import stale_retry

DEFAULT_TIMEOUT = 40

logger = logging.getLogger(__name__)


class Element(object):

    def __init__(self, page, locator, select_by=By.XPATH):
        self.page = page
        self.driver = page.driver
        self._select_by = select_by
        self._locator = locator
        self.wait = WebDriverWait(self.driver, 10)
        self.validate_selector()

    @property
    def element(self):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, self._locator)))

    def text(self, timeout=const.Wait.SHORT_WAIT):
        return self.get_text(timeout=timeout)

    def send_keys(self, text, timeout=const.Wait.SHORT_WAIT):
        self.wait_until_visible(timeout=timeout).send_keys(text)

    def send_keys_and_hit_enter(self, text):
        self.send_keys(text)
        self.send_keys(Keys.ENTER)

    def clear(self, timeout=const.Wait.SHORT_WAIT):
        element = self.locate(timeout)  # type: WebElement
        element.clear()

    def hover_over_element(self):
        hover = ActionChains(self.driver)
        hover.move_to_element(self.locate()).perform()

    def js_click(self, timeout=0):
        self.driver.execute_script("arguments[0].click();", self.locate(timeout))

    def naked_click(self, timeout=const.Wait.MID_WAIT):
        self.wait_until_clickable(timeout).click()

    def toggle(self, value=None):
        selected = self.is_selected()
        if value != selected:
            self.click()
        elif value is None:
            self.click()

    def is_selected(self):
        return self.wait_until_visible().is_selected()

    def validate_selector(self):
        try:
            if self._select_by in [By.XPATH, By.CSS_SELECTOR]:
                self.driver.find_element(self._select_by, self._locator)
        except InvalidSelectorException:
            raise
        except NoSuchElementException:
            return
        except:
            raise

    def format(self, *text):
        """

        :param text:
        :return: format the locator
        """
        class_name = self.__class__
        new_element = class_name(self.driver, self._select_by, self._locator.format(*text))
        return new_element

    def append(self, locator):
        """

        :param locator:
        :return: append locator to an existing one
        """
        class_name = self.__class__
        new_element = class_name(self.driver, self._select_by, self._locator + locator)
        return new_element

    def locate(self, timeout=DEFAULT_TIMEOUT):
        presence_of_element_located = expected_conditions.presence_of_element_located((self._select_by, self._locator))
        return WebDriverWait(self.driver, timeout).until(presence_of_element_located,
                                                         f'Cannot locate element with {self._select_by}: {self._locator}')

    def exists(self, timeout=0):
        """
        :param timeout:
        :return: Boolean if element present
        """
        try:
            self.locate(timeout)
            return True
        except:
            return False

    def is_visible(self, timeout=0):
        """
        :param timeout:
        :return: Boolean if element is visible
        """
        try:
            self.wait_until_visible(timeout)
            return True
        except:
            return False

    def is_active(self, timeout=0):
        """
        :param timeout:
        :return: Boolean if element class has 'active'
        """
        element = self.locate(timeout)
        return "active" in str(element.get_attribute('class'))

    def is_clickable(self, timeout=0):
        """
        :param timeout:
        :return: Boolean if element is clickable
        """
        try:
            self.wait_until_clickable(timeout)
            return True and 'disabled' not in self.__getattribute__('class')
        except:
            return False

    def list(self, timeout=0):
        presence_of_elements_located = expected_conditions.presence_of_all_elements_located(
            (self._select_by, self._locator))
        try:
            error = f'Cannot find any element with {self._select_by} {self._locator} after {timeout}'
            results = WebDriverWait(self.driver, timeout).until(presence_of_elements_located, error)
        except (NoSuchElementException, TimeoutException):
            results = []
        return results

    def locate_all(self, timeout=DEFAULT_TIMEOUT):
        presence_of_elements_located = expected_conditions.presence_of_all_elements_located(
            (self._select_by, self._locator))
        return WebDriverWait(self.driver, timeout).until(presence_of_elements_located,
                                                         f"Cannot find any element with {self._select_by} {self._locator}, after {timeout} seconds")

    def wait_until_visible(self, timeout=DEFAULT_TIMEOUT, pool_frequency=.5):
        return WebDriverWait(self.driver, timeout, pool_frequency).until(
            expected_conditions.visibility_of_element_located((self._select_by, self._locator)),
            f'Element {self._locator} is still not visible after waiting for {timeout} seconds')

    def wait_until_invisible(self, timeout=DEFAULT_TIMEOUT, pool_frequency=.5):
        return WebDriverWait(self.driver, timeout, pool_frequency).until(
            expected_conditions.invisibility_of_element_located((self._select_by, self._locator)),
            f'Element {self._locator} is still visible after waiting for {timeout} seconds')

    def wait_until_clickable(self, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            expected_conditions.element_to_be_clickable((self._select_by, self._locator)),
            f'Element {self._locator} is still not clickable after waiting for {timeout} seconds')

    def wait_until_text_present_in_element(self, text, timeout=DEFAULT_TIMEOUT):
        time.sleep(1)
        return WebDriverWait(self.driver, timeout).until(
            expected_conditions.text_to_be_present_in_element
            ((self._select_by, self._locator), text),
            f'Element {self._locator} still does not contain text {text} after waiting for {timeout} seconds')

    def wait_for_loading(self, start_loading_timeout=1, stop_loading_timeout=DEFAULT_TIMEOUT):
        try:
            logger.debug(f"Waiting {start_loading_timeout} secs for Element to start loading")
            start = time.time()
            self.wait_until_visible(timeout=stop_loading_timeout, pool_frequency=.1)
        except:
            end = time.time()
            logger.debug(f"Waiting for Element to start loading TIMED OUT after [{end}-{start}] seconds")
        else:
            end = time.time()
            logger.debug(f"Element started LOADING in [{end}-{start}] secs")
        logger.debug(f"Waiting [{stop_loading_timeout}] secs for Element to finish loading")
        start = time.time()
        self.wait_until_invisible(timeout=stop_loading_timeout, pool_frequency=0.1)
        end = time.time()
        logger.debug(f"Element finished LOADING in [{end}-{start}] seconds")

    def getByLocator(self):
        by_locator = (self._select_by, self._locator)
        return by_locator

    def scroll_into_view(self):
        click_script = "arguments[0].scrollIntoView(true);"
        self.driver.execute_script(click_script, self.locate())

    def click(self, timeout=DEFAULT_TIMEOUT, index=0):
        start_time = time.time()
        timeleft = 1

        while timeleft > 0:
            try:
                self.wait_until_visible(timeout)
                self.wait_until_clickable(timeout).click()
                break
            except WebDriverException as e:
                if "Other element would receive the click" in str(e):
                    time.sleep(1)
                else:
                    raise
            timeleft = timeout - (time.time() - start_time)
            if timeleft <= 0:
                raise Exception(f"Element {self._locator} is still not clickable"
                                f"after waiting for {timeout} seconds.")

    def get_text(self, timeout=DEFAULT_TIMEOUT):
        self.wait_until_visible(timeout)
        return self.locate().text

    @stale_retry()
    def get_attribute(self, name):
        return self.locate().get_attribute(name)

    def move_to(self, index=0, timeout=DEFAULT_TIMEOUT):
        ActionChains(self.driver).move_to_element(self.locate_all()[index]).perform()

    def double_click(self):
        ActionChains(self.driver).double_click(self.locate()).perform()


class DropdownElement(Element):
    def __int__(self, page, locator):
        super().__init__(page, locator)
        self.page = page
        self.driver = page.driver
        self.locator = locator

    @property
    def value(self):
        select = Select(self.element)
        return select.first_selected_option.text

    @value.setter
    def value(self, option_label):
        select = Select(self.element)
        select.select_by_visible_text(option_label)


class NavMenuSelector(Element):

    def __int__(self, page, locator):
        super().__init__(page, locator)
        self.page = page
        self.driver = page.driver
        self.locator = locator

    @property
    def value(self):
        raise AttributeError('Getter unsupported for nav menu, use only setter for click.')

    @value.setter
    def value(self, menu_item_text):
        xpath = f"//ul[@class='nav-menu']//li//a[text()='{menu_item_text}']"
        element = NavMenuSelector(page=self, locator=xpath)
        element.wait_until_clickable().click()


class TextAreaElement(Element):

    def fill_out_field(self, text, num_delete=50):
        self.click()
        delete_key = Keys.BACKSPACE * num_delete + Keys.DELETE * num_delete
        self.send_keys(delete_key)
        self.send_keys(text)


class ElementList(Element):

    @stale_retry()
    def get_all_text(self, timeout=DEFAULT_TIMEOUT):
        all_text = []
        elements = self.locate_all(timeout)
        for element in elements:
            all_text.append(element.text)
        return all_text

    @stale_retry(3)
    def click_child_by_text(self, text, timeout=DEFAULT_TIMEOUT):
        """

        :param text: look to click element with the text
        :param timeout: list to be present/visible
        :return: True if found element with the given text and clicked it, else False
        """
        start_time = time.time()
        time_left = 1
        while time_left >= 0:
            elements = self.locate_all(timeout)
            time_left = timeout - (time.time() - start_time)
            if time_left > 0:
                self.wait_until_clickable(timeout)
            for element in elements:
                if text in element.text:
                    element.click()
                    return True
            time_left = timeout - (time.time() - start_time)
        return False

    @stale_retry()
    def click_all(self, text=None, selected=None, seconds_between_click=0, timeout=DEFAULT_TIMEOUT):
        """

        :param text: if specified, clicks only element that contains the text
        :param selected: if selected, either True or False, clicks only elements that has the same value for its selected state
        :param seconds_between_click: num of secs between click
        :param timeout: timeout list to be present
        :return: None
        """
        start_time = time.time()
        if len(self.locate_all(timeout)) > 0:
            timeout = timeout - (time.time() - start_time)
            if timeout > 0:
                self.wait_until_clickable(int(timeout))
            index = 0
            while True:
                elements = self.locate_all(int(timeout))
                if index >= len(elements):
                    break
                else:
                    element = elements[index]
                    index += 1
                    if text is not None and text not in element.text:
                        continue
                    if selected is not None and selected is not element.is_selected():
                        continue
                    if seconds_between_click > 0:
                        time.sleep(seconds_between_click)

                    if element.is_displayed():
                        element.click()
