#coding=utf-8
import sys
import unittest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from base import AppiumBaseHelper

class FacebookHelper(unittest.TestCase, AppiumBaseHelper):
    def __init__(self, driver, platformName, platformVersion):
        AppiumBaseHelper.__init__(self, driver, platformName, platformVersion)

    def login(self, username, password):
        bClickedLogin = False
        bGrantedPermission = False

        # wait login transition
        self.wait_transition(1)

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

        self.logger.info('Try to locate facebook login button by text')
        if self.click_button_with_text([u'登入']) == True:
            bClickedLogin = True
        if bClickedLogin is False: raise NoSuchElementException('could not identify facebook login button in the page')

        # wait for loading
        self.wait_transition(1)

        # grant facebook permission
        self.logger.info('Try to locate facebook permission button by text')
        if self.click_button_with_text([u'繼續', u'確定']) == True:
            bGrantedPermission = True
        if bGrantedPermission is False: raise NoSuchElementException('could not identify facebook grant permission button in the page')

        # wait for loading
        self.wait_transition(1)

        return True


class SysHelper(unittest.TestCase, AppiumBaseHelper):
    def __init__(self, driver, platformName, platformVersion):
        AppiumBaseHelper.__init__(self, driver, platformName, platformVersion)
        self.fb = FacebookHelper(driver, platformName, platformVersion)

    def start_soocii(self):
        # The function does not work due to missing android:exported=”true” for the activity
        # self.driver.start_activity('me.soocii.socius.staging', 'me.soocii.socius.core.ui.MainActivity')
        self.press_recent_apps_key()
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
        for el in items:
            if self.app_name in el.text:
                el.click()
                return
        raise NoSuchElementException('could not identify soocii in recent apps')

    def start_setting_page(self):
        self.driver.start_activity('com.android.settings', 'com.android.settings.Settings')

    # support for sony z3, samsung note5
    def __enable_usage_access_sony_z3(self):
        # Usage access permission
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
        for el in items:
            self.logger.info(u'text of located element: {}'.format(el.text))
            if self.app_name in el.text:
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

    # support for sony z3, asus zenfone2
    def __enable_usage_access_sony_m4(self):
        # Usage access permission
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
        for el in items:
            self.logger.info(u'text of located element: {}'.format(el.text))
            if self.app_name in el.text:
                # 1st level of setting
                el.click()
                # Confirmation
                self.logger.info('identify confirmation dialog')
                el = self.wait.until(EC.presence_of_element_located((By.ID, "alertTitle")))
                self.logger.info('identified confirmation dialog')
                if el is not None:
                    if self.click_button_with_text(["OK", u"確定"]) is True:
                        # Back to Soccii App
                        self.press_back_key()
                        self.logger.info('enabled usage access in sony m4')
                        return True
                # could not identify alert dialog
                self.logger.info('could not identify confirmation dialog')
                raise NoSuchElementException('could not identify confirmation dialog')

    def enable_usage_access(self):
        # click on confirm "請選擇Soocii，並將可存取使用情形打開"
        self.click_textview_with_id("confirm")

        try:
            self.logger.info('try enable usage access in sony m4')
            self.__enable_usage_access_sony_m4()
        except:
            self.logger.info('caught exception: {}'.format(sys.exc_info()[0]))
            try:
                self.logger.info('try enable usage access in sony z3, samsung note5')
                self.__enable_usage_access_sony_z3()
            except:
                raise

    def enable_draw_on_top_layer(self):
        # click on confirm "請選擇允許在其他應用程式上層繪製內容，並將其打開"
        self.click_textview_with_id("confirm")

        # draw on top layer permission
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
        for el in items:
            self.logger.info(u'text of located element: {}'.format(el.text))
            el.click()

        # Back to Soccii App
        self.press_back_key()
        self.logger.info('enabled draw on top layer')
        return True

    def login_facebook_account(self, username, password):
        self.logger.info('username: {}, password: {}'.format(username, password))
        self.fb.login(username, password)
