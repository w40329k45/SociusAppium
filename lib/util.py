#coding=utf-8
import unittest

from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

import SociusAppium.config as config

class Util(unittest.TestCase):
    def __init__(self, driver, wait, window_size):
        assert driver is not None
        assert wait is not None
        assert window_size is not None
        self.driver = driver
        self.wait = wait
        self.window_size = window_size

    def wait_for_transition(self, wait_time=3):
        sleep(float(wait_time))

    def press_back_key(self):
        # sending 'Back' key event
        self.driver.press_keycode(4)
        self.wait_for_transition(1)

    def press_home_key(self):
        # sending 'Home' key event
        self.driver.press_keycode(3)
        self.wait_for_transition(1)

    def press_recent_apps_key(self):
        # sending 'Recent Apps' key event
        self.driver.press_keycode(187)
        self.wait_for_transition(1)

    def click_button_with_text(self, text):
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.Button")))
        for el in items:
            if el.text in text:
                el.click()
                return

    def start_soocii(self):
        # The function does not work due to missing android:exported=”true” for the activity
        # self.driver.start_activity('me.soocii.socius.staging', 'me.soocii.socius.core.ui.MainActivity')
        self.press_recent_apps_key()
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
        for el in items:
            if config.APP_NAME in el.text:
                el.click()
                return
        raise TimeoutException('could not identify soocii in recent apps')

    def start_setting_page(self):
        self.driver.start_activity('com.android.settings', 'com.android.settings.Settings')

    def catch_screen(self, prefix):
        with open(prefix+"_page_source.xml", "w") as xml_file:
            xml_file.write(self.driver.page_source.encode('utf8'))
        self.driver.save_screenshot(prefix+'_screenshot.png')

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
            print el.text
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
                break

    def __enable_usage_access_sony_m4(self, appName=config.APP_NAME):
        # Usage access permission
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))

        for el in items:
            print el.text
            if appName in el.text:
                # 1st level of setting
                el.click()

                # Confirmation
                allBtns = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.Button")))
                self.assertEqual(2, len(allBtns))
                for el in allBtns:
                    if el.text == "OK":
                        el.click()

                        # Back to Soccii App
                        self.press_back_key()
                        break
                break

    def enable_usage_access(self, appName=config.APP_NAME):
        # wait for tutorial
        self.wait_for_transition(5)

        try:
            self.__enable_usage_access_sony_m4(appName=appName)
        except:
            try:
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

    def login_facebook_account(self, username, password, must=True):
        # wait login transition
        self.wait_for_transition()

        try:
            # Webview-based
            allEditText = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.EditText")))
            self.assertTrue(len(allEditText)==2)
            self.assertIsNotNone(allEditText)
            # User name field
            el = allEditText[0]
            print el.text
            el.send_keys(username)
            self.driver.hide_keyboard()
            # Password field
            el = allEditText[1]
            print el.text
            el.send_keys(password)
            self.driver.hide_keyboard()

            allBtns = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.Button")))
            self.assertTrue(len(allBtns)==1)
            # Login button
            el = allBtns[0]
            print el.get_attribute('name')
            el.click()

            # wait for loading
            self.wait_for_transition()

            # Has granted facebook permission
            xpath = "//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[2]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[2]/android.view.View[1]/android.view.View[2]/android.widget.Button[1]"
            okBtn = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            self.assertIsNotNone(okBtn)
            okBtn.click()

            return True
        except:
            if must is False:
                return False
            raise
