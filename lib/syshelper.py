#coding=utf-8
import unittest

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

import SociusAppium.config as config

from base import AppiumBaseHelper

class FacebookHelper(unittest.TestCase, AppiumBaseHelper):
    def __init__(self, driver, window_size):
        AppiumBaseHelper.__init__(self, driver, window_size)

    def login(self, username, password):
        bClickedLogin = False

        # wait login transition
        self.wait_transition()

        # Webview-based
        allEditText = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.EditText")))
        self.assertTrue(len(allEditText)==2)
        self.assertIsNotNone(allEditText)
        # User name field
        el = allEditText[0]
        self.logger.info(u'text of located element: {}'.format(el.text))
        el.send_keys(username)
        self.driver.hide_keyboard()
        # Password field
        el = allEditText[1]
        self.logger.info(u'text of located element: {}'.format(el.text))
        el.send_keys(password)
        self.driver.hide_keyboard()

        allBtns = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.Button")))
        for el in allBtns:
            self.logger.info(u'text of located element: {}'.format(el.get_attribute('name')))
            if el.get_attribute('name').strip() in [u"登入"]:
                el.click()
                bClickedLogin = True
                break
        if bClickedLogin is False: raise NoSuchElementException('could not identify facebook login button in the page')

        # wait for loading
        self.wait_transition()

        # grant facebook permission
        try:
            # Not grant facebook permission yet
            xpath = "//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[2]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.widget.Button[1]"
            btn = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            btn.click()
        except:
            # Has granted facebook permission
            xpath = "//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[2]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[2]/android.widget.Button[1]"
            btn = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            btn.click()

class SysHelper(unittest.TestCase, AppiumBaseHelper):
    def __init__(self, driver, window_size):
        AppiumBaseHelper.__init__(self, driver, window_size)
        self.fb = FacebookHelper(driver, window_size)

    def start_soocii(self):
        # The function does not work due to missing android:exported=”true” for the activity
        # self.driver.start_activity('me.soocii.socius.staging', 'me.soocii.socius.core.ui.MainActivity')
        self.press_recent_apps_key()
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
        for el in items:
            if config.APP_NAME in el.text:
                el.click()
                return
        raise NoSuchElementException('could not identify soocii in recent apps')

    def start_setting_page(self):
        self.driver.start_activity('com.android.settings', 'com.android.settings.Settings')

    # support for sony z3, samsung note5
    def __enable_usage_access_sony_z3(self, appName=config.APP_NAME):
        try:
            # try tap on "Continue"
            x = self.window_size["width"] * 0.5

            y = self.window_size["height"] * 0.80
            self.driver.tap([(x, y)], 500)

            y = self.window_size["height"] * 0.85
            self.driver.tap([(x, y)], 500)

            y = self.window_size["height"] * 0.9
            self.driver.tap([(x, y)], 500)
        except WebDriverException:
            # continue with expected exception
            pass

        # Usage access permission
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
        for el in items:
            self.logger.info(u'text of located element: {}'.format(el.text))
            if appName in el.text:
                # 1st level of setting
                el.click()

                # 2nd level of setting
                switch = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "android.widget.Switch")))
                self.assertIsNotNone(switch)
                switch.click()

                # Back to Soccii App
                self.press_back_key()
                self.press_back_key()
                self.logger.info('enabled usage access in sony z3, samsung note5')
                return True

    def __enable_usage_access_sony_m4(self, appName=config.APP_NAME):
        # Usage access permission
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
        for el in items:
            self.logger.info(u'text of located element: {}'.format(el.text))
            if appName in el.text:
                # 1st level of setting
                el.click()
                # Confirmation
                if self.click_button_with_text("OK") is True:
                    # Back to Soccii App
                    self.press_back_key()
                    self.logger.info('enabled usage access in sony m4')
                    return True

    def enable_usage_access(self, appName=config.APP_NAME):
        # wait for tutorial
        self.wait_transition(5)
        try:
            self.logger.info('try enable usage access in sony m4')
            self.__enable_usage_access_sony_m4(appName=appName)
        except Exception as e:
            self.logger.info('caught exception: {}'.format(str(e)))
            try:
                self.logger.info('try enable usage access in sony z3, samsung note5')
                self.__enable_usage_access_sony_z3(appName=appName)
            except:
                raise

    def allow_system_permissions(self):
        wait_time = config.WAIT_TIME
        wait = WebDriverWait(self.driver, wait_time)
        try:
            count = 1
            while True:
                allBtns = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.Button")))
                #self.assertEqual(2, len(allBtns))
                if len(allBtns) == 0: return
                for el in allBtns:
                    if el.text in ["Allow", u"允許"]:
                        el.click()
                        break
                if count > 5:
                    raise TimeoutException()
                count = count + 1
                # decrease wait time
                wait_time = wait_time / 2 if wait_time > 2 else 1
                wait = WebDriverWait(self.driver, wait_time)
        except TimeoutException:
            # continue with expected exception
            pass
        except NoSuchElementException:
            # continue with expected exception
            pass

    def login_facebook_account(self, username, password):
        self.logger.info('username: {}, password: {}'.format(username, password))
        self.fb.login(username, password)
