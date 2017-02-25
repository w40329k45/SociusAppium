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
from selenium.common.exceptions import TimeoutException

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class SociusTests(unittest.TestCase):
    def setUp(self):
        wait_time = 5

        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.0'
        desired_caps['deviceName'] = 'Android Emulator'
        #desired_caps['full-reset'] = True
        desired_caps['app'] = PATH(
            'soocii_v0.0.1034_google_2017_0221_1046_staging.apk'
        )

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(wait_time)
        self.wait = WebDriverWait(self.driver, wait_time)

    def tearDown(self):
        # remove app
        #self.driver.remove_app('me.soocii.socius.staging')
        self.driver.close_app()

        # end the session
        self.driver.quit()

    def catch_failure(self, prefix):
        with open(prefix+"_page_source.xml", "w") as xml_file:
            xml_file.write(self.driver.page_source.encode('utf8'))
        self.driver.save_screenshot(prefix+'_screenshot.png')

    def login_facebook_account(self, username, password, must=True):
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

    def start_usage_access_setting_page(self):
        self.driver.start_activity('com.android.settings', 'com.android.settings.Settings')

    # The function does not due to proguard
    def start_soocii(self):
        self.driver.start_activity('me.soocii.socius.staging', 'me.soocii.socius.core.ui.MainActivity')

    def enable_usage_access_sony_z3(self, appName="Soocii", must=False):
        self.start_usage_access_setting_page()
        self.catch_failure('settings')
        try:
            # Usage access permission
            items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))

            for el in items:
                if appName in el.text:
                    el.click()
                    break
        except:
            if must == False:
                return False
            raise

    def enable_usage_access(self, appName="Soocii", must=False):
        # wait for tutorial
        sleep(5)

        try:
            # Usage access permission
            xpath = "//android.view.View[1]/android.widget.FrameLayout[2]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.ListView[1]/*"
            items = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

            for el in items:
                app = el.find_element_by_class_name("android.widget.TextView")
                self.assertIsNotNone(app)
                if appName in app.text:
                    app.click()
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

    def allow_system_permissions(self, must=False):
        try:
            while True:
                allBtns = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.Button")))
                self.assertEqual(2, len(allBtns))
                for el in allBtns:
                    if el.text == "Allow":
                        el.click()
                        break            
        except:
            if must == False:
                return False
            raise

    def skip_guide_mark(self, must=False):
        # wait login transition
        sleep(5)

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

    def first_login_and_enable_usage_access(self):
        try:
            #self.start_usage_access_setting_page()
            #self.enable_usage_access_sony_z3(must=True)

            # Facebook Login button on Soocii
            el = self.wait.until(EC.presence_of_element_located((By.XPATH, "//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[1]/android.widget.Button[1]")))
            self.assertIsNotNone(el)
            el.click()

            self.login_facebook_account("doctorfamily.mobi@gmail.com", "soocii@2016")
            self.allow_system_permissions()
            self.enable_usage_access(must=True)
            self.press_back_key()
        except:
            self.catch_failure("except")
            raise

    def login_with_facebook_webview(self):
        try:
            #self.start_usage_access_setting_page()

            # Facebook Login button on Soocii
            el = self.wait.until(EC.presence_of_element_located((By.XPATH, "//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[1]/android.widget.Button[1]")))
            self.assertIsNotNone(el)
            el.click()

            presence = self.login_facebook_account("doctorfamily.mobi@gmail.com", "soocii@2016")
            self.skip_guide_mark(must=presence)
        except:
            self.catch_failure("except")
            raise

    # def test_login_existing_facebook_account(self):
    #     # Facebook Login button on Soocii
    #     el = self.wait.until(EC.presence_of_element_located((By.XPATH, "//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[1]/android.widget.Button[1]")))
    #     self.assertIsNotNone(el)
    #     el.click()

    #     self.login_facebook_account("doctorfamily.mobi@gmail.com", "drmobile@123456")

    @pytest.mark.first
    def test_first_login_and_enable_usage_access(self):
        self.first_login_and_enable_usage_access()

    def test_facebook_login(self):
        self.login_with_facebook_webview()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SociusTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

