#coding=utf-8
import logging

from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from packaging import version

# app name
APP_NAME="Soocii-staging"
# package name
PACKAGE_NAME="me.soocii.socius.staging"
# defautl wait time in second
WAIT_TIME=5

class AppiumBaseHelper():
    def __init__(self, driver, platformName, platformVersion):
        assert driver is not None
        self.logger = logging.getLogger()
        self.driver = driver
        self.window_size = self.driver.get_window_size()
        self.wait = WebDriverWait(self.driver, WAIT_TIME)
        self.platformName = platformName
        self.platformVersion = platformVersion

    @property
    def app_name(self):
        return APP_NAME

    @property
    def package_name(self):
        return PACKAGE_NAME

    def isAndroid5(self):
        if self.platformName == 'Android':
            if version.parse(self.platformVersion) >= version.parse('5.0.0') and version.parse(self.platformVersion) < version.parse('6.0.0'):
                return True
        return False

    def wait_transition(self, wait_time):
        sleep(float(wait_time))

    def press_back_key(self):
        # sending 'Back' key event
        self.driver.press_keycode(4)
        self.wait_transition(0.5)

    def press_home_key(self):
        # sending 'Home' key event
        self.driver.press_keycode(3)
        self.wait_transition(0.5)

    def press_recent_apps_key(self):
        # sending 'Recent Apps' key event
        self.driver.press_keycode(187)
        self.wait_transition(0.5)

    def click_button_with_text(self, text):
        allBtns = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.Button")))
        for btn in allBtns:
            self.logger.info(u'Check button: {} ({})'.format(btn.text, btn.get_attribute('name')))
            if btn.text:
                if btn.text.strip() in text:
                    btn.click()
                    return True
            # support attribute for content-desc
            if btn.get_attribute('name'):
                if btn.get_attribute('name').strip() in text:
                    btn.click()
                    return True
        return False

    def click_button_with_id(self, id):
        btn = self.wait.until(EC.presence_of_element_located((By.ID, id)))
        if btn is None: return False
        btn.click()
        return  True

    def click_textview_with_text(self, text):
        allTxtViews = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
        for txtView in allTxtViews:
            if txtView.text in text:
                txtView.click()
                return True
            elif text[0] in txtView.text:
                txtView.click()
                return True
            elif text[1] in txtView.text:
                txtView.click()
                return True
        return False

    def click_textview_with_id(self, id):
        txtView = self.wait.until(EC.presence_of_element_located((By.ID, id)))
        if txtView is None: return False
        txtView.click()
        return True

    def send_text_with_id(self, id, text):
        field = self.wait.until(EC.presence_of_element_located((By.ID, id)))
        field.clear()
        field.send_keys(text)
        if id in "input_soocii_id_text":
            self.driver.keyevent(66)
        try:
            self.driver.hide_keyboard()
        except:
            # ignore any exception due to asus zenfone does not always show soft keyword when sending keys
            pass

    # tap on screen and swipe from right to left
    def swipe_left(self):
        left_x = self.window_size["width"] * 0.1
        right_x = self.window_size["width"] * 0.9
        center_y = self.window_size["height"] * 0.8
        self.driver.swipe(start_x=right_x, start_y=center_y, end_x=left_x, end_y=center_y, duration=500)
        self.wait_transition(0.5)

    # tap on screen and swipe from left to right
    def swipe_right(self):
        left_x = self.window_size["width"] * 0.1
        right_x = self.window_size["width"] * 0.9
        center_y = self.window_size["height"] * 0.5
        self.driver.swipe(start_x=left_x, start_y=center_y, end_x=right_x, end_y=center_y, duration=500)
        self.wait_transition(0.5)

    def swipe_down(self):
        center_x=self.window_size["width"]*0.5
        top_y=self.window_size["height"]*0.4
        button_y=self.window_size["height"]*0.9
        self.driver.swipe(start_x=center_x,start_y=top_y,end_x=center_x,end_y=button_y,duration=350)
        self.wait_transition(4)

    def swipe_up(self):
        center_x=self.window_size["width"]*0.5
        top_y=self.window_size["height"]*0.4
        button_y=self.window_size["height"]*0.9
        self.driver.swipe(start_x=center_x,start_y=button_y,end_x=center_x,end_y=top_y,duration=350)
        self.wait_transition(4)

    def swipe_hash(self):
        left_x = self.window_size["width"] * 0.1
        right_x = self.window_size["width"] * 0.9
        center_y = self.window_size["height"] * 0.56
        self.driver.swipe(start_x=right_x, start_y=center_y, end_x=left_x, end_y=center_y, duration=500)
        self.wait_transition(0.5)

    def get_text_with_id(self, id):
        text = self.wait.until(EC.presence_of_element_located((By.ID, id)))
        return text.text

    def capture_screen(self, prefix):
        self.driver.save_screenshot(prefix+'_screenshot.png')
        with open(prefix+"_page_source.xml", "w") as xml_file:
            xml_file.write(self.driver.page_source.encode('utf8'))

    def allow_system_permissions(self, max_counts=1):
        wait_time = 5
        wait = WebDriverWait(self.driver, wait_time)
        try:
            count = 1
            while True:
                allBtns = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.Button")))
                if len(allBtns) == 0: return
                for el in allBtns:
                    if el.text in ["Allow", u"允許"]:
                        el.click()
                        break
                if count > max_counts:
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