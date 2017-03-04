#coding=utf-8
import logging
import SociusAppium.config as config

from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class AppiumBaseHelper():
    def __init__(self, driver, window_size):
        assert driver is not None
        assert window_size is not None
        self.logger = logging.getLogger()
        self.driver = driver
        self.window_size = window_size
        self.wait = WebDriverWait(self.driver, config.WAIT_TIME)

    def wait_transition(self, wait_time=3):
        sleep(float(wait_time))

    def press_back_key(self):
        # sending 'Back' key event
        self.driver.press_keycode(4)
        self.wait_transition(1)

    def press_home_key(self):
        # sending 'Home' key event
        self.driver.press_keycode(3)
        self.wait_transition(1)

    def press_recent_apps_key(self):
        # sending 'Recent Apps' key event
        self.driver.press_keycode(187)
        self.wait_transition(1)

    def click_button_with_text(self, text):
        btn = self.wait.until(EC.presence_of_element_located((By.NAME, text)))
        btn.click()
        return True

    def click_button_with_id(self, id):
        btn = self.wait.until(EC.presence_of_element_located((By.ID, id)))
        btn.click()

    def send_text_with_id(self, id, text):
        field = self.wait.until(EC.presence_of_element_located((By.ID, id)))
        field.clear()
        field.send_keys(text)
        self.driver.hide_keyboard()

    # tap on screen and swipe from right to left
    def swipe_left(self):
        left_x = self.window_size["width"] * 0.1
        right_x = self.window_size["width"] * 0.9
        center_y = self.window_size["height"] * 0.5
        self.driver.swipe(start_x=right_x, start_y=center_y, end_x=left_x, end_y=center_y, duration=500)
        self.wait_transition(1)

    # tap on screen and swipe from left to right
    def swipe_right(self):
        left_x = self.window_size["width"] * 0.1
        right_x = self.window_size["width"] * 0.9
        center_y = self.window_size["height"] * 0.5
        self.driver.swipe(start_x=left_x, start_y=center_y, end_x=right_x, end_y=center_y, duration=500)
        self.wait_transition(1)


    def get_text_with_id(self, id):
        text = self.wait.until(EC.presence_of_element_located((By.ID, id)))
        return text.text

    def capture_screen(self, prefix):
        self.driver.save_screenshot(prefix+'_screenshot.png')
        with open(prefix+"_page_source.xml", "w") as xml_file:
            xml_file.write(self.driver.page_source.encode('utf8'))
