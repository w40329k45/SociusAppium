#coding=utf-8
import os
import unittest

from time import sleep

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

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
