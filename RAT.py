#coding=utf-8
import os
import pytest
import unittest

from time import sleep
from appium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException

import config
from lib.util import Util
from lib.socius import Socius

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

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
        self.driver.implicitly_wait(config.WAIT_TIME)
        self.wait = WebDriverWait(self.driver, config.WAIT_TIME)
        self.window_size = self.driver.get_window_size()

        self.util = Util(self.driver, self.wait, self.window_size)
        self.socius = Socius(self.driver, self.wait, self.window_size)

    def tearDown(self):
        # remove app
        self.driver.close_app()

        # end the session
        self.driver.quit()

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

    # support for sony z3, samsung note5
    def enable_usage_access_sony_z3(self, appName=config.APP_NAME, must=False):
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

                    # Back to Soccii App
                    self.util.press_back_key()
                    self.util.press_back_key()
                    break
        except:
            if must == False:
                return False
            raise

    def enable_usage_access_sony_m4(self, appName=config.APP_NAME, must=False):
        try:
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
                            self.util.press_back_key()
                            break
                    break
        except:
            if must == False:
                return False
            raise

    def enable_usage_access(self, appName=config.APP_NAME, must=False):
        # wait for tutorial
        self.wait_for_transition(5)

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

    @pytest.mark.first
    def test_fresh_install_and_enable_usage_access(self):
        try:
            # Facebook Login button on Soocii
            self.socius.click_facebook_login_button()

            self.login_facebook_account("doctorfamily.mobi@gmail.com", "soocii@2016")
            self.allow_system_permissions()
            # only need to enable usage access once
            self.enable_usage_access(must=True)
            self.socius.skip_guide_mark()
        except:
            self.util.catch_screen("except")
            raise

    def test_login_existing_facebook_account(self):
        try:
            # Facebook Login button on Soocii
            self.socius.click_facebook_login_button()

            self.login_facebook_account("doctorfamily.mobi@gmail.com", "soocii@2016")
            self.allow_system_permissions()
            self.socius.skip_guide_mark()
            self.socius.click_logout_button()
        except:
            self.util.catch_screen("except")
            raise

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SociusTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

