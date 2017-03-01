#coding=utf-8
import unittest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import SociusAppium.config as config
from util import Util

class Socius(unittest.TestCase):
    def __init__(self, driver, wait, window_size):
        assert driver is not None
        assert wait is not None
        assert window_size is not None
        self.driver = driver
        self.wait = wait
        self.window_size = window_size
        self.util = Util(driver, wait, window_size)

    def get_facebook_login_button(self):
        # Facebook Login button on Soocii
        return self.wait.until(EC.presence_of_element_located((By.XPATH, "//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.RelativeLayout[1]/android.widget.Button[1]")))

    def click_facebook_login_button(self):
        el = self.get_facebook_login_button()
        self.assertIsNotNone(el)
        el.click()
        self.util.wait_for_transition(1)

    def start_logger_activity(self):
        # The function does not work due to missing android:exported=”true” for the activity
        # self.driver.start_activity('me.soocii.socius.staging', 'me.soocii.socius.core.logger.LogCaptureActivity')
        el = self.wait.until(EC.presence_of_element_located((By.ID, "tv_app_version")))
        self.assertIsNotNone(el)
        for i in range(1, 6): el.click()
        self.driver.open_notifications()
        self.util.wait_for_transition(1)
        # Click on "Soocii Logger" or expand Soocii notification
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
        for el in items:
            print el.text
            if el.text == "Soocii Logger":
                print "Soocii Logger"
                el.click()
                self.util.wait_for_transition(1)
                return
        # Expand Soocii notification
        for el in items:
            if "Soocii" in el.text:
                el.click()
                self.util.wait_for_transition(1)
                # Click on "Soocii Logger"
                items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
                for el in items:
                    if el.text == "Soocii Logger":
                        el.click()
                        self.util.wait_for_transition(1)
                        return

    def click_revoke_facebook(self):
        self.start_logger_activity()
        revokeBtn = self.wait.until(EC.presence_of_element_located((By.ID, "btn_revoke_fb")))
        self.assertIsNotNone(revokeBtn)
        revokeBtn.click()

    def click_delete_account_button(self):
        self.start_logger_activity()
        deleteBtn = self.wait.until(EC.presence_of_element_located((By.ID, "btn_delete_account")))
        self.assertIsNotNone(deleteBtn)
        deleteBtn.click()
        self.util.click_button_with_text("Logout")

    def click_logout_button(self):
        self.start_logger_activity()
        logoutBtn = self.wait.until(EC.presence_of_element_located((By.ID, "btn_logout")))
        self.assertIsNotNone(logoutBtn)
        logoutBtn.click()
        self.util.click_button_with_text("Logout")

    def skip_guide_mark(self):
        # wait login transition
        self.util.wait_for_transition(1)

        el = self.wait.until(EC.presence_of_element_located((By.ID, "guide")))
        self.assertIsNotNone(el)

        # tap on screen 4 times
        center_x = self.window_size["width"] / 2
        center_y = self.window_size["height"] / 2
        for i in range(1, 5):
            self.driver.tap([(center_x, center_y)], 500)
