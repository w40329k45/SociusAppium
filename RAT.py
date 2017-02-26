#coding=utf-8
import os
import pytest
import unittest

from time import sleep
from appium import webdriver

# Next 3 imports are just for enabling 'explicitly_wait_for'
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

# app name
APP_NAME="Soocii-staging"
# package name
PACKAGE_NAME="me.soocii.socius.staging"
# defautl wait time in second
WAIT_TIME=5

class SociusTests(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.0'
        desired_caps['deviceName'] = 'Android Emulator'
        #desired_caps['full-reset'] = True
        desired_caps['app'] = PATH(
            'soocii_v0.0.1034_google_2017_0221_1046_staging.apk'
        )

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(WAIT_TIME)
        self.wait = WebDriverWait(self.driver, WAIT_TIME)

    def tearDown(self):
        # remove app
        self.driver.close_app()

        # end the session
        self.driver.quit()

    def catch_failure(self, prefix):
        with open(prefix+"_page_source.xml", "w") as xml_file:
            xml_file.write(self.driver.page_source.encode('utf8'))
        self.driver.save_screenshot(prefix+'_screenshot.png')

    def wait_for_transition(self, wait_time=3):
        sleep(float(wait_time))

    def login_facebook_account(self, username, password, must=True):
        # wait login transition
        self.wait_for_transition()

        try:
            # Webview-based
            allEditText = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.EditText")))
            self.assertEqual(2, len(allEditText))
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
            self.assertEqual(1, len(allBtns))
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

    def press_back_key(self):
        # sending 'Back' key event
        self.driver.press_keycode(3)

    def press_home_key(self):
        # sending 'Home' key event
        self.driver.press_keycode(3)
        self.wait_for_transition(1)

    def press_recent_apps_key(self):
        # sending 'Recent Apps' key event
        self.driver.press_keycode(187)
        self.wait_for_transition(1)

    def start_usage_access_setting_page(self):
        self.driver.start_activity('com.android.settings', 'com.android.settings.Settings')

    # The function does not due to proguard
    def start_soocii(self):
        # self.driver.start_activity('me.soocii.socius.staging', 'me.soocii.socius.core.ui.MainActivity')
        self.press_recent_apps_key()
        try:
            items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
            for el in items:
                if APP_NAME in el.text:
                    el.click()
                    return
            raise TimeoutException('could not identify soocii in recent apps')
        except:
            raise

    def enable_usage_access_sony_z3(self, appName=APP_NAME, must=False):
        try:
            # tap on "Continue"
            window_size = self.driver.get_window_size()
            x = window_size["width"] * 0.5
            y = window_size["height"] * 0.85
            self.driver.tap([(x, y)], 500)
        except WebDriverException:
            # continue with expected exception
            pass

        try:
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
                    break
        except:
            if must == False:
                return False
            raise

    def enable_usage_access_sony_m4(self, appName=APP_NAME, must=False):
        try:
            # Usage access permission
            items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))

            for el in items:
                print el.text
                if appName in el.text:
                    # 1st level of setting
                    el.click()
                    break

            # Confirmation
            allBtns = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.Button")))
            self.assertEqual(2, len(allBtns))
            for el in allBtns:
                if el.text == "OK":
                    el.click()
                    break

            return True
        except:
            if must == False:
                return False
            raise

    def enable_usage_access(self, appName=APP_NAME, must=False):
        # wait for tutorial
        self.wait_for_transition()

        try:
            self.enable_usage_access_sony_m4(appName=appName, must=must)
        except:
            try:
                self.enable_usage_access_sony_z3(appName=appName, must=must)
            except:
                if must == False:
                    return False
                raise

    def allow_system_permissions(self):
        wait_time = WAIT_TIME
        wait = WebDriverWait(self.driver, wait_time)
        try:
            while True:
                allBtns = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.Button")))
                self.assertEqual(2, len(allBtns))
                for el in allBtns:
                    if el.text == "Allow":
                        el.click()
                        break            
                # decrease wait time
                wait_time = wait_time / 2 if wait_time > 2 else 1
                wait = WebDriverWait(self.driver, wait_time)
        except TimeoutException:
            # continue with expected exception
            pass

    def skip_guide_mark(self, must=False):
        # wait login transition
        self.wait_for_transition(1)

        try:
            el = self.wait.until(EC.presence_of_element_located((By.ID, "guide")))
            self.assertIsNotNone(el)

            # tap on screen 4 times
            window_size = self.driver.get_window_size()
            center_x = window_size["width"] / 2
            center_y = window_size["height"] / 2
            for i in range(1, 5):
                self.driver.tap([(center_x, center_y)], 500)
        except:
            if must == False:
                return False
            raise

    @pytest.mark.first
    def test_fresh_install_and_enable_usage_access(self):
        try:
            # Facebook Login button on Soocii
            el = self.wait.until(EC.presence_of_element_located((By.XPATH, "//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[1]/android.widget.Button[1]")))
            self.assertIsNotNone(el)
            el.click()

            self.login_facebook_account("doctorfamily.mobi@gmail.com", "soocii@2016")
            self.allow_system_permissions()
            self.enable_usage_access(must=True)
        except:
            self.catch_failure("except")
            raise

    def test_login_existing_facebook_account(self):
        try:
            # Facebook Login button on Soocii
            el = self.wait.until(EC.presence_of_element_located((By.XPATH, "//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[1]/android.widget.Button[1]")))
            self.assertIsNotNone(el)
            el.click()

            presence = self.login_facebook_account("doctorfamily.mobi@gmail.com", "soocii@2016")
            self.allow_system_permissions()
            self.skip_guide_mark(must=presence)
            self.press_home_key()
            self.start_soocii()
        except:
            self.catch_failure("except")
            raise

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SociusTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

