#coding=utf-8
import unittest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from base import AppiumUtil
from util import Util

class Socius(unittest.TestCase, AppiumUtil):
    def __init__(self, driver, window_size):
        AppiumUtil.__init__(self, driver, window_size)
        self.util = Util(driver, window_size)

    def get_facebook_login_button(self):
        # Facebook Login button on Soocii
        return self.wait.until(EC.presence_of_element_located((By.XPATH, "//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[1]/android.widget.Button[1]")))

    def click_facebook_login_button(self):
        el = self.get_facebook_login_button()
        self.assertIsNotNone(el)
        el.click()
        self.wait_transition(1)

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
            print el.text
            if el.text == "Soocii Logger":
                print "Soocii Logger"
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
        self.click_button_with_text("Logout")

    def skip_guide_mark(self):
        # wait login transition
        self.wait_transition(1)

        el = self.wait.until(EC.presence_of_element_located((By.ID, "guide")))
        self.assertIsNotNone(el)

        # tap on screen 4 times
        center_x = self.window_size["width"] / 2
        center_y = self.window_size["height"] / 2
        for i in range(1, 5):
            self.driver.tap([(center_x, center_y)], 500)

    def create_account(self, displayName, soociiId):
        self.send_text_with_id("display_name_value", displayName)
        self.send_text_with_id("soocii_id_value", soociiId)
        # email_value
        self.click_button_with_id("register")
        # transition to next page
        self.wait_transition(1)

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

    def is_newsfeed(self):
        return self.__visibility_of_textview(["Newsfeed", u"即時動態"])

    def is_friendlist(self):
        return self.__visibility_of_textview(["Friends", u"好友頻道"])

    def is_aboutme(self):
        return self.__visibility_of_textview(["Me", u"關於我"])

    def swipe_to_newsfeed(self):
        return

    def swipe_to_friendlist(self):
        return

    def swipe_to_aboutme(self):
        if self.is_aboutme():
            pass
        elif self.is_newsfeed():
            self.swipe_left()
            self.swipe_left()
        elif self.is_frindlist():
            self.swipe_left()
        else:
            raise NoSuchElementException('could not identify [aboutme] page')

    def get_personal_info(self):
        self.swipe_to_aboutme()
        self.click_button_with_id("tv_about_me_more")
        displayName = self.get_text_with_id("tv_display_name")
        soociiId = self.get_text_with_id("tv_soocii_id")
        # go back to main page
        self.press_back_key()
        return displayName, soociiId
