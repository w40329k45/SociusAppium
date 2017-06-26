#coding=utf-8
import unittest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from base import AppiumBaseHelper

class SociusHelper(unittest.TestCase, AppiumBaseHelper):
    def __init__(self, driver, platformName, platformVersion):
        AppiumBaseHelper.__init__(self, driver, platformName, platformVersion)

    def click_facebook_login_button(self):
        self.click_button_with_id("btn_fb_login")
        self.wait_transition(1)

    def click_create_new_account_using_email_button(self):
        self.click_button_with_id("create_email_account")
        self.wait_transition(0.5)

    def click_login_by_email_link(self):
        self.click_button_with_id("login_by_email")
        self.wait_transition(0.5)

    def start_logger_activity(self):
        # The function does not work due to missing android:exported=”true” for the activity
        # self.driver.start_activity('me.soocii.socius.staging', 'me.soocii.socius.core.logger.LogCaptureActivity')
        el = self.wait.until(EC.presence_of_element_located((By.ID, "tv_app_version")))
        self.assertIsNotNone(el)
        for i in range(1, 6): el.click()
        self.driver.open_notifications()
        self.wait_transition(1)
        # Click on "Soocii Logger" or expand Soocii notification
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
        for el in items:
            self.logger.info(u'Check text view: {}'.format(el.text))
            if el.text == "Soocii Logger":
                self.logger.info(u'Found text view: {}'.format(el.text))
                el.click()
                self.wait_transition(1)
                return
        # Expand Soocii notification
        for el in items:
            if "Soocii" in el.text:
                el.click()
                self.wait_transition(1)
                # Click on "Soocii Logger"
                items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
                for el in items:
                    if el.text == "Soocii Logger":
                        el.click()
                        self.wait_transition(1)
                        return

    def click_revoke_facebook(self):
        self.start_logger_activity()
        self.click_button_with_id("btn_revoke_fb")

    def click_delete_account_button(self):
        self.start_logger_activity()
        self.click_button_with_id("btn_delete_account")

    def click_delete_and_revoke_account_button(self):
        self.start_logger_activity()
        self.click_button_with_id("btn_delete_account")
        self.click_button_with_id("btn_revoke_fb")

    def click_logout_button(self):
        self.start_logger_activity()
        self.click_button_with_id("btn_logout")
        # logout confirmation
        self.click_button_with_text(["Logout", u"登出"])

    def click_require_permission_button(self):
        # only require for Android6+
        if self.isAndroid5():
            return
        self.click_textview_with_text(u"確認")
        # allow all system permissions
        self.allow_system_permissions(4)

    def skip_floating_ball_guide_mark(self):
        el = self.wait.until(EC.presence_of_element_located((By.ID, "permission_video")))
        self.assertIsNotNone(el)

        # tap on screen to skip
        center_x = self.window_size["width"] / 2
        center_y = self.window_size["height"] / 2
        self.driver.tap([(center_x, center_y)], 500)

    def login_account(self, email, pwd):
        self.send_text_with_id("email_value", email)
        self.logger.info('sent email: {}'.format(email))
        self.send_text_with_id("password_value", pwd)
        self.logger.info('sent password: {}'.format(pwd))
        self.click_button_with_id("login")
        # transition to next page
        self.wait_transition(0.5)

    def create_account(self, displayName, soociiId, email=None, pwd=None, confirmEmail=None, confirmPwd=None):
        self.send_text_with_id("display_name_value", displayName)
        self.logger.info('sent display name: {}'.format(displayName))
        self.send_text_with_id("soocii_id_value", soociiId)
        self.logger.info('sent soocii id: {}'.format(soociiId))
        # email_value
        if email is not None:
            self.send_text_with_id("email_value", email)
            #self.send_text_with_id("email_confirm_value", email if confirmEmail is None else confirmEmail)
            self.logger.info('sent email: {}'.format(email))
        # password_value
        if pwd is not None:
            self.send_text_with_id("password_value", pwd)
            #self.send_text_with_id("password_confirm_value", pwd if confirmPwd is None else confirmPwd)
            self.logger.info('sent password: {}'.format(pwd))
        self.click_button_with_id("register")
        # transition to next page
        self.wait_transition(0.5)

    def add_followers(self):
        self.click_button_with_id("add_follow_confirm")
        # transition to next page
        self.wait_transition(1)

    def __visibility_of_textview(self, text):
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
        for el in items:
            if el.text in text:
                return True
        return False

    def is_discover(self):
        return self.__visibility_of_textview(["Discover", u"探索"])

    def is_newsfeed(self):
        return self.__visibility_of_textview(["Newsfeed", u"即時動態"])

    def is_aboutme(self):
        return self.__visibility_of_textview(["Me", u"關於我"])

    def swipe_to_newsfeed(self):
        return

    def swipe_to_friendlist(self):
        return

    def swipe_to_aboutme(self):
        self.click_textview_with_id("icon_profile")

    def get_personal_info(self):
        self.swipe_to_aboutme()
        self.click_button_with_id("tv_about_me_more")
        displayName = self.get_text_with_id("tv_display_name")
        soociiId = self.get_text_with_id("tv_soocii_id")
        # go back to main page
        self.press_back_key()
        return displayName, soociiId
