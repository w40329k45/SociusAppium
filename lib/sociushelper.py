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
        self.click_textview_with_text([u"確認","Confirm"])
        # allow all system permissions
        self.allow_system_permissions(4)

    def click_onlinevideocard(self):
        self.click_button_with_id("iv_thumbnail")
        self.wait_transition(2)
        self.press_back_key()

    def click_videocard(self):
        # self.swipe_loading()
        # self.swipe_loading()
        self.click_button_with_id("rl_post_card")
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

    def is_message(self):# today
        check = self.wait.until(EC.presence_of_all_elements_located((By.ID,"rootLayout")))
        if check is None:
            return False
        return True

    def is_discover(self):
        return self.__visibility_of_textview(["Discovery", u"探索"])

    def is_newsfeed(self):
        return self.__visibility_of_textview(["Newsfeed", u"即時動態"])

    def is_aboutme(self):
        return self.__visibility_of_textview(["Me", u"關於我"])

    def is_FAQ(self):
        return self.__visibility_of_textview(["FAQ", u"常見問題"])

    def is_Contact(self):
        return self.__visibility_of_textview(["Contact", u"聯絡我們"])

    def is_faqwebview(self):
        wv=self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"android.webkit.WebView")))
        if wv is None:
            return False
        return True

    def swpie_share_posts(self):# today
        self.click_textview_with_id("tv_shares")
        self.wait_transition(1)

    def swipe_share_posts_to_soocii(self):
        self.click_button_with_id("menu_share_to_soocii")
        self.wait_transition(1)

    def swipe_share_posts_to_otherapp(self):
        self.click_button_with_id("menu_share_to_other")
        self.wait_transition(1)

    def swipe_discover(self):
        self.wait_transition(2)
        self.click_button_with_id("tv_discovery")
        self.wait_transition(1)
        return

    def swipe_to_newsfeed(self):
        self.wait_transition(2)
        self.click_button_with_id("tv_feed")
        return

    def swipe_to_friendlist(self):
        self.wait_transition(2)
        self.click_button_with_id("iv_invite_icon")
        return

    def swipe_to_aboutme(self):
        self.wait_transition(2)
        self.click_textview_with_id("icon_profile")

    def swipe_to_support(self):
        self.wait_transition(2)
        self.click_button_with_id("iv_help_icon")

    def swipe_to_fans(self):
        self.wait_transition(2)
        self.click_textview_with_text([u"粉絲","Follower"])

    def swipe_to_suggest(self):
        self.wait_transition(2)
        self.click_textview_with_text(["Suggest",u"用戶推薦"])

    def swipe_to_SearchId(self):
        self.wait_transition(2)
        self.click_textview_with_text([u"ID搜尋","ID Search"])

    def swipe_to_faq(self):
        self.wait_transition(2)
        self.click_textview_with_id("tv_faq")

    def swipe_to_contact(self):
        self.wait_transition(2)
        self.click_textview_with_id("tv_contact")

    def swipe_refresh(self):
        self.wait_transition(2)
        self.swipe_down(350)

    def swipe_loading(self):
        self.wait_transition(2)
        self.swipe_up(350)

    def swipe_post_sandwish(self):
        self.wait_transition(2)
        self.click_button_with_id("iv_more")

    def swipe_post_edit(self):
        self.wait_transition(2)
        self.click_button_with_id("menu_edit")

    def swipe_choose_video(self):
        self.wait_transition(2)
        self.click_textview_with_text([u"影音","Video"])
    def swipe_edit(self):
        left_x = self.window_size["width"] * 0.06
        right_x = self.window_size["width"] * 0.5
        center_y = self.window_size["height"] * 0.9
        self.driver.swipe(start_x=left_x, start_y=center_y, end_x=right_x, end_y=center_y, duration=500)
        self.wait_transition(1)

    def swipe_edit_back(self):
        left_x = self.window_size["width"] * 0.06
        right_x = self.window_size["width"] * 0.5
        center_y = self.window_size["height"] * 0.9
        self.driver.swipe(start_x=right_x, start_y=center_y, end_x=left_x, end_y=center_y, duration=350)
        self.wait_transition(1)

    def edit_cover(self):
        left_x = self.window_size["width"] * 0.06
        right_x = self.window_size["width"] * 0.5
        center_y = self.window_size["height"] * 0.9
        self.driver.swipe(start_x=right_x, start_y=center_y, end_x=left_x, end_y=center_y, duration=350)
        self.wait_transition(1)


    def swipe_posts(self):# today
        #soocii & local ID is deffirend
        self.wait_transition(2.5)
        try:
            posts_bt = self.wait.until(EC.presence_of_element_located((By.ID,"iv_screenshot")))
        except :
            posts_bt = self.wait.until(EC.presence_of_element_located((By.ID,"iv_thumbnail")))
        finally :
            posts_bt.click()
            self.wait_transition(1)

    def swipe_like(self):# today
        self.wait_transition(1)
        like_bt = self.wait.until(EC.presence_of_element_located((By.ID,"iv_like")))
        like_bt.click()
        self.wait_transition(1)


    def swipe_and_send_message(self):# today
        message_bt = self.wait.until(EC.presence_of_element_located((By.ID,"message_edit_text")))
        message_bt.click()
        self.wait_transition(1)
        self.send_text_with_id("message_edit_text","this is qa message")
        self.wait_transition(1.5)
        send_message_bt = self.wait.until(EC.presence_of_element_located((By.ID,"outbox")))
        send_message_bt.click()
        self.wait_transition(1.5)

    def swipe_aboutme_video(self):#today
        video_bt = self.wait.until(EC.presence_of_all_elements_located((By.ID,"iv_video")))
        if video_bt is None:
            return False
        video_bt[0].click()
        self.wait_transition(2)


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
        videocard=self.wait.until(EC.presence_of_element_located((By.ID,"rl_post_card")))
        if videocard is None:
            return False
        else:
            return True

    def chech_share_posts(self):
        if self.get_text_with_id("tv_msg") in "this is share post testing":
            return True
        return False

    def check_like_num(self):#today
        check_like_tv = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"android.widget.TextView")))
        self.wait_transition(0.5)
        for items in check_like_tv:
            if "like" in items.text:
                return items.text.split(" ")[0]
            elif u"個棒" in items.text:
                return items.text.split(" ")[0]

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

        items = self.wait.until(EC.presence_of_all_elements_located((By.ID,"text")))
        d=[]
        for ii in range(1,3):

            for el in items:
                elname=el.text
                if el.text not in d:
                    d.append(el.text)

                    el.click()
                    self.wait_transition(2.5)

                    videonum=self.wait.until(EC.presence_of_all_elements_located((By.ID,"iv_video_play")))
                    vtag=self.wait.until(EC.presence_of_all_elements_located((By.ID,"tv_tag")))
                    if len(videonum)<4:
                        return False
                    else:
                        for al in vtag:
                            if al.text not in elname:
                                return False

                    self.wait_transition(2.5)
                    self.press_back_key()
                    self.wait_transition(2.5)
                else:
                    return
            self.swipe_hash()
            self.wait_transition(2.5)
            items = self.wait.until(EC.presence_of_all_elements_located((By.ID,"text")))

    def check_zendesk(self):
        self.assertTrue(self.is_FAQ())
        self.assertTrue(self.is_Contact())

    def check_faq(self):
        self.swipe_to_faq()
        self.wait_transition(4)
        self.assertTrue(self.is_faqwebview())
        self.wait_transition(2)
        self.press_back_key()

    def check_contact(self):
        self.swipe_to_contact()
        #click add button
        self.click_textview_with_id("activity_request_list_add_icon")
        bbt=self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,"android.widget.ImageButton")))
        bbt.click()
        #click add button
        self.click_textview_with_id("activity_request_list_add_icon")
        self.send_text_with_id("contact_fragment_description","ignore this ! automation test!")
        self.wait_transition(1.5)
        self.click_textview_with_id("fragment_contact_zendesk_menu_done")
        self.wait_transition(1.5)
        self.press_back_key()

    def check_video_and_photo_icon(self):
        vpicons=self.wait.until(EC.presence_of_all_elements_located((By.ID,"tv_action")))
        keyw=[u"影音","Viedo",u"圖片","Image"]
        for vpicon in vpicons:
            if vpicon.text in keyw:

                return True
        return False

    def click_choose_album(self):
        self.click_textview_with_text([u"相簿","Photos"])

    def click_alwaysbutton(self):
        self.click_button_with_id("button_always")

    def click_confirm_recommended_celebrity(self):
        # wait for recommended list is loaded
        self.wait_transition(8)
        self.click_button_with_id("add_follow_confirm")
        self.wait_transition(3)

    def click_camera_floatball(self):
        self.wait_transition(5)
        #dp=px*160/dpi
        #px=dp*dpi/160
        center_x = self.window_size["width"]
        if center_x == 720 : self.driver.tap([(45, 650)], 500)
        elif center_x == 1080 : self.driver.tap([(50, 980)], 500)
        else : self.driver.tap([(100, 1300)], 500)


    def click_open_fab_button(self):
        self.click_button_with_id("fab_live")
        self.wait_transition(2)

    def click_viedo_to_share(self):#today
        self.swipe_aboutme_video()#click video

        self.click_button_with_id("btn_trim_complete")
        self.wait_transition(1)
        self.click_button_with_id("btn_trim_complete")
        self.wait_transition(1)#click next button x2

        self.send_text_with_id("upload_edittext","video from about me")#posts message
        self.wait_transition(1.5)

        self.click_textview_with_id("tv_share")#click share button
        self.wait_transition(1.5)


    def choice_game(self):
        self.click_textview_with_text(["Snake Off","Snake Off"])
        self.wait_transition(1)

    def setting_live(self):
        self.click_button_with_id("ib_broadcast_icon_camera_switch")
        self.wait_transition(3)
        self.click_button_with_id("btn_friend_broadcast")
        self.wait_transition(1)
        self.click_button_with_id("button1")
        self.wait_transition(20)

    def broadcast(self,message):
        self.click_button_with_id("iv_menu_icon_chat")
        self.wait_transition(1)
        self.click_button_with_id("messageEditText")
        self.wait_transition(1)
        self.send_text_with_id("messageEditText", message)
        self.logger.info('sent message: {}'.format(message))
        self.wait_transition(5)
        self.click_button_with_id("sendButton")
        self.wait_transition(2)

    def change_camera(self):
        self.click_button_with_id("iv_menu_icon_camera")
        self.wait_transition(10)

    def stop_live(self):
        self.click_button_with_id("iv_menu_icon_stop")
        self.wait_transition(5)

    def go_to_post(self):
        self.click_button_with_id("tv_go")

    def share_live_record(self, upload,x):
        #self.click_button_with_id("tv_go")
        self.wait_transition(1)
        self.click_button_with_id("upload_edittext")
        self.wait_transition(1)
        self.send_text_with_id("upload_edittext", upload+str(x+1))
        self.logger.info('sent upload: {}'.format(upload+str(x+1)))
        self.wait_transition(3)
        self.click_button_with_id("tv_share")
        self.wait_transition(15)

    def back_soocii(self):
        self.click_button_with_id("iv_menu_icon_back")
        self.wait_transition(1)

    def refresh_aboutme(self):
        self.swipe_down(350)
        self.wait_transition(3)

    def check_post_title(self,text):
        #check title
        postmsg=self.wait.until(EC.presence_of_element_located((By.ID,"tv_msg")))
        posttitle=postmsg.text
        posttitle.index(text)
        self.wait_transition(2)

    def check_post(self):

        #click post
        postcard=self.wait.until(EC.presence_of_all_elements_located((By.ID,"iv_thumbnail")))
        postcard[0].click()
        self.wait_transition(2)
        #click sandwish button
        self.swipe_post_sandwish()
        self.wait_transition(1)
        #click edit button
        self.swipe_post_edit()
        self.wait_transition(1)
        #edit
        self.send_text_with_id("upload_edittext","edit post")
        self.wait_transition(1)
        #click confirm
        self.click_button_with_id("tv_share")
        self.wait_transition(2)
        self.check_post_title("edit post")

    def check_and_refresh_share_posts(self,text):#today
        for x in range(3):
            self.swipe_refresh()
            self.wait_transition(3)
        self.check_post_title(text)

    def check_share_otherapp_posts(self):
        self.swipe_posts()
        self.swpie_share_posts()
        self.swipe_share_posts_to_otherapp()
        shoth=self.wait.until(EC.presence_of_element_located((By.ID,"title")))
        if shoth is None:
            return False
        return True

    def choose_video(self):
        #choose folder
        photofolder=self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"android.widget.RelativeLayout")))
        photofolder[0].click()
        self.wait_transition(2)
        #choose video
        if self.isAndroid5():
            avideo=self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"android.view.View")))
        else:
            avideo=self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"android.view.ViewGroup")))
        avideo[1].click()
        self.wait_transition(2)

    def new_local_video_post(self):
        self.wait_transition(5)
        #add local video
        self.swipe_choose_video()
        self.wait_transition(2)
        try:
            #check choose google album
            self.assertFalse(self.click_choose_album())
        except:
            #if don't have the button
            self.click_alwaysbutton()
        else:
            #if have the button,do not thing
            pass

        self.choose_video()
        #click next*2
        self.click_button_with_id("btn_trim_complete")
        self.wait_transition(1)
        self.click_button_with_id("btn_trim_complete")
        self.wait_transition(2)
        #keyin title
        self.send_text_with_id("upload_edittext","upload video from local")
        self.click_textview_with_id("tv_share")
        self.wait_transition(20)
        self.swipe_refresh()
        #check title
        self.check_post_title("upload video from local")

    def input_send_share_message(self):# today
        self.send_text_with_id("upload_edittext","this is share post testing")
        self.wait_transition(1.5)
        self.click_textview_with_id("action_share")
        self.wait_transition(1.5)
        self.press_back_key()
        self.wait_transition(1)

    def edit_live_record(self):
        x = self.window_size["width"] * 0.8
        y = self.window_size["height"] * 0.15
        self.swipe_edit()
        self.swipe_edit_back()
        self.wait_transition(2)
        self.driver.tap([(x,y)],500)
        self.wait_transition(2)
        self.edit_cover()
        self.wait_transition(3)


    def edit_next(self):
        x = self.window_size["width"] * 0.9
        y = self.window_size["height"] * 0.1
        self.driver.tap([(x,y)],500)

    def download_live_record(self):

        self.click_button_with_id("tv_download")
        self.wait_transition(10)
        self.press_home_key()
        self.wait_transition(1)
        self.driver.open_notifications()
        self.wait_transition(1)
        #self.swipe()
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
        for el in items:
            self.logger.info(u'Check text view: {}'.format(el.text))
            if el.text == "Tap to edit":
                self.logger.info(u'Found text view: {}'.format(el.text))
                self.wait_transition(2)
                self.click_textview_with_text(["Tap to edit","Tap to edit"])
                self.wait_transition(1)
                return
        # Expand Soocii notification
        for el in items:
            if "Soocii" in el.text:
                el.click()
                self.wait_transition(1)
                #Click on "Soocii Logger"
                items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
                for el in items:
                    if el.text == "Tap to edit":
                        el.click()
                        self.wait_transition(1)
                        return
        self.wait_transition(1)

    def goto_RTMP(self):
        self.swipe_to_newsfeed()
        self.wait_transition(30)
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
        for el in items:
            self.logger.info(u'Check text view: {}'.format(el.text))
            if el.text == "test stream":
                self.logger.info(u'Found text view: {}'.format(el.text))
                self.wait_transition(2)
                self.click_textview_with_text(["test stream","test stream"])
                self.wait_transition(1)
                return

    def gotochat_with_discovery(self):
        self.swipe_discover()
        x=1
        while x==1:
            items = self.wait.until(EC.presence_of_all_elements_located((By.ID, "tv_streaming_message")))
            for el in items:
                self.logger.info(u'Check text view: {}'.format(el.text))
                if el.text == "test stream":
                    self.logger.info(u'Found text view: {}'.format(el.text))
                    el.click()
                    x=2
                    return


    def chat_live(self,a):
        x = self.window_size["width"] * 0.5
        y = self.window_size["height"] * 0.5
        self.wait_transition(20)
        self.driver.tap([(x,y)],350)
        self.wait_transition(2)
        self.click_button_with_id("messageEditText")
        self.wait_transition(2)
        self.send_text_with_id("messageEditText", a)
        self.logger.info('sent message: {}'.format(a))
        self.click_button_with_id("sendButton")
        self.wait_transition(1)

    def click_sharelink_button(self):
        self.click_button_with_id("shareButton")
        self.wait_transition(5)
        self.press_back_key()

    def click_viewer_button(self):
        self.wait_transition(5)
        self.click_button_with_id("img_btn_check_viewers")
        self.wait_transition(1)

    def leave_live(self):
        self.press_back_key()
        self.press_back_key()
        self.wait_transition(2)


    def check_viewer_name(self):
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
        for el in items:
            self.logger.info(u'Check text view: {}'.format(el.text))
            if el.text == "chnnnnnnnb":
                self.logger.info(u'Found text view: {}'.format(el.text))
                self.wait_transition(2)
                return True
        return False



    def goto_RTMP(self):
        self.swipe_to_newsfeed()
        self.wait_transition(30)
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
        for el in items:
            self.logger.info(u'Check text view: {}'.format(el.text))
            if el.text == "test stream":
                self.logger.info(u'Found text view: {}'.format(el.text))
                self.wait_transition(2)
                self.click_textview_with_text(["test stream","test stream"])
                self.wait_transition(1)
                return

    def gotochat_with_discovery(self):
        self.swipe_discover()
        x=1
        while x==1:
            items = self.wait.until(EC.presence_of_all_elements_located((By.ID, "tv_streaming_message")))
            for el in items:
                self.logger.info(u'Check text view: {}'.format(el.text))
                if el.text == "test stream":
                    self.logger.info(u'Found text view: {}'.format(el.text))
                    el.click()
                    x=2
                    return


    def chat_live(self,a):
        x = self.window_size["width"] * 0.5
        y = self.window_size["height"] * 0.5
        self.wait_transition(20)
        self.driver.tap([(x,y)],350)
        self.wait_transition(2)
        self.click_button_with_id("messageEditText")
        self.wait_transition(2)
        self.send_text_with_id("messageEditText", a)
        self.logger.info('sent message: {}'.format(a))
        self.click_button_with_id("sendButton")
        self.wait_transition(1)

    def click_sharelink_button(self):
        self.click_button_with_id("shareButton")
        self.wait_transition(5)
        self.press_back_key()

    def click_viewer_button(self):
        self.wait_transition(5)
        self.click_button_with_id("img_btn_check_viewers")
        self.wait_transition(1)

    def leave_live(self):
        self.press_back_key()
        self.press_back_key()
        self.wait_transition(2)


    def check_viewer_name(self):
        items = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "android.widget.TextView")))
        for el in items:
            self.logger.info(u'Check text view: {}'.format(el.text))
            if el.text == "chnnnnnnnb":
                self.logger.info(u'Found text view: {}'.format(el.text))
                self.wait_transition(2)
                return True
        return False
