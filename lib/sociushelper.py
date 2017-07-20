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
        self.click_textview_with_text(u"確認","Confirm")
        # allow all system permissions
        self.allow_system_permissions(4)

    def click_onlinevideocard(self):
        self.click_button_with_id("iv_thumbnail")
        self.wait_transition(2)
        self.press_back_key()

    def click_videocard(self):
        self.swipe_loading()
        self.swipe_loading()
        self.click_button_with_id("iv_video_play")
        self.wait_transition(2)
        self.press_back_key()

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
        self.wait_transition(1)

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

    def is_discover(self):
        return self.__visibility_of_textview(["Discovery", u"探索"])

    def is_newsfeed(self):
        return self.__visibility_of_textview(["Newsfeed", u"即時動態"])

    def is_aboutme(self):
        return self.__visibility_of_textview(["Me", u"關於我"])

    def swipe_discover(self):
        self.click_button_with_id("tv_discovery")
        self.wait_transition(1)
        return

    def swipe_to_newsfeed(self):
        self.click_button_with_id("tv_feed")
        return

    def swipe_to_friendlist(self):
        self.click_button_with_id("iv_invite_icon")
        return

    def swipe_to_aboutme(self):
        self.click_textview_with_id("icon_profile")

    def swipe_to_support(self):
        self.click_button_with_id("iv_help_icon")

    def swipe_to_fans(self):
        self.click_textview_with_text([u"粉絲","Follower"]) 

    def swipe_to_suggest(self):
        self.click_textview_with_text(["Suggest",u"用戶推薦"]) 
           
    def swipe_to_SearchId(self):
        self.click_textview_with_text([u"ID搜尋","ID Search"])

    def swipe_refresh(self):
        self.swipe_down()

    def swipe_loading(self):
        self.swipe_up()

    def get_newsfeed_info(self):
        self.swipe_to_newsfeed()
        feedcard = self.wait.until(EC.presence_of_all_elements_located((By.ID,"ll_post_card")))
        if feedcard is None:
            return False
        else:
            return True

    def get_personal_info(self):
        self.swipe_to_aboutme()
        self.click_button_with_id("tv_about_me_more")
        displayName = self.get_text_with_id("tv_display_name")
        soociiId = self.get_text_with_id("tv_soocii_id")
        # go back to main page
        self.press_back_key()
        return displayName, soociiId

    def get_friendlist_info(self):
        self.swipe_to_friendlist()
        friends_video = self.wait.until(EC.presence_of_all_elements_located((By.ID, "video")))
        if friends_video is None:
         return False
        else:
            return True

    def get_idsearch(self):
        self.send_text_with_id("input_soocii_id_text","scheng1")
        self.wait_transition(1.5)
        self.press_back_key()

    def get_videocard(self):
        videocard=self.wait.until(EC.presence_of_element_located((By.ID,"iv_video_play")))
        if videocard is None:
            return False
        else:
            return True

    def check_aboutme(self,exdisplayname):
        self.swipe_to_aboutme()
        displayName = self.get_text_with_id("tv_display_name")
        if exdisplayname in displayName:
            return True
        else:
            return False
    def check_support(self):
        self.swipe_to_support()
        supportname = self.get_text_with_id("tv_display_name")
        if "Support" in supportname:
            self.press_back_key()
            return True
        else:
            return False

    def check_suggest(self):
        self.swipe_to_suggest()
        suggestbutton =self.wait.until(EC.presence_of_all_elements_located((By.ID,"facebook_invite")))
        if suggestbutton is None:
            return False
        else:
            return True

    def check_hashtag(self):
        tagtext=self.wait.until(EC.presence_of_all_elements_located((By.ID,"text")))

        i=0
        for  el in tagtext:
            self.click_textview_with_text(el.text)
            self.wait_transition(2)
            i=i+1
            videonum=self.wait.until(EC.presence_of_all_elements_located((By.ID,"iv_video_play")))
            vtag=self.wait.until(EC.presence_of_all_elements_located((By.ID,"tv_tag")))
            if len(videonum)<4:
                return False
            # for al in vtag:
            #     if el.text != al.text:
            #         return False
            self.press_back_key()
            if i == 2:
                self.swipe_hash()
                i=0
                self.wait_transition(2)
        return True



