# -*- coding: utf-8 -*-
#coding=utf-8
import os
import re
import sys
import pytest
import logging
import unittest
import subprocess
import time

from appium import webdriver

import config
from RAT import *

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

path1 = "./test_resources/."

# logger
logger = logging.getLogger()
logFormatter = logging.Formatter(
    '[%(asctime)-15s][%(filename)s][%(funcName)s#%(lineno)d] %(message)s')
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(logFormatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

class LiveTests(BaseTests):
    def test_openlive(self):
        try:
            # #login_with_email
            # self.sociushelper.click_login_by_email_link()
            # self.sociushelper.login_account("channing@gmail.com", "zxasqw123")

            # self.sociushelper.click_require_permission_button()

            expectedDisplayName=config.EXISTING_FACEBOOK_ACCOUNT1_DISPLAYNAME
            expectedSoociiId=config.EXISTING_FACEBOOK_ACCOUNT1_SOOCIIID

            # Facebook Login button on Soocii
            self.sociushelper.click_facebook_login_button()
            self.syshelper.login_facebook_account(config.EXISTING_FACEBOOK_ACCOUNT1, config.EXISTING_FACEBOOK_ACCOUNT1_PWD)

            # confirm acquiring permission dialog
            self.sociushelper.click_require_permission_button()

            #open_streaming 10 times
            # for x in range(10):
            self.sociushelper.click_open_fab_button()
            self.sociushelper.click_accept()
            self.sociushelper.choice_game()
            self.sociushelper.setting_live()
            self.sociushelper.click_camera_floatball()
            self.sociushelper.broadcast("hi welcome to my broadcast")
            for y in range(3):
                self.sociushelper.change_camera()
            #share post
            self.sociushelper.stop_live()
            self.sociushelper.go_to_post()
            self.sociushelper.share_live_record("broadcast",x)
            self.sociushelper.click_camera_floatball()
            self.sociushelper.back_soocii()
            self.sociushelper.swipe_to_aboutme()
            self.sociushelper.refresh_aboutme()

        except :
            self.logger.info('caught exception: {}'.format(sys.exc_info()[0]))
            self.syshelper.capture_screen("test_open_live")
            raise
    def test_download(self):
        try:
            #login_with_email
            self.sociushelper.click_login_by_email_link()
            self.sociushelper.login_account("channing@gmail.com", "zxasqw123")

            self.sociushelper.click_require_permission_button()
            #open_streaming 10 times
            for x in range(10):
                self.sociushelper.click_open_fab_button()
                try:
                    self.sociushelper.click_accept()     
                except:
                    pass
                self.sociushelper.click_accept()
                self.sociushelper.choice_game()
                self.sociushelper.setting_live()
                self.sociushelper.click_camera_floatball()
                self.sociushelper.stop_live()
                self.sociushelper.go_to_post()
                #download live record and edit
                self.sociushelper.download_live_record()
                self.sociushelper.edit_live_record()
                self.sociushelper.edit_next()
                #get time
                localtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                self.sociushelper.share_live_record(localtime+"download",x)
                self.syshelper.start_snake_off()
                self.sociushelper.click_camera_floatball()
                self.sociushelper.back_soocii()
                self.sociushelper.swipe_to_aboutme()
                self.sociushelper.refresh_aboutme()


        except :
            self.logger.info('caught exception: {}'.format(sys.exc_info()[0]))
            self.syshelper.capture_screen("test_download")
            raise

    def test_viewer(self):
        try:
            self.sociushelper.click_login_by_email_link()
            self.sociushelper.login_account("channing@gmail.com", "zxasqw123")
            self.sociushelper.click_require_permission_button()
            for x in range(10):
                #go to live in discover

                self.sociushelper.gotochat_with_discovery()
                #viewer test
                self.sociushelper.chat_live("i love this game")
                self.sociushelper.click_sharelink_button()
                self.sociushelper.click_viewer_button()
                self.assertTrue(self.sociushelper.check_viewer_name())
                self.sociushelper.click_viewer_button()
                self.sociushelper.leave_live()

        except :
            self.logger.info('caught exception: {}'.format(sys.exc_info()[0]))
            self.syshelper.capture_screen("test_viewer")
            raise

    def test_game(self):
        try:
            self.sociushelper.click_login_by_email_link()
            self.sociushelper.login_account("channing999@gmail.com", "zxasqw123")
            self.sociushelper.click_require_permission_button()
            #test ilve record screenshot in game
            #open snake off
            opensnakeoff()
            self.sociushelper.click_camera_floatball()
            self.sociushelper.screenshot_ingame()
            self.sociushelper.click_camera_floatball()
            self.sociushelper.open_live_ingame()
            self.sociushelper.click_camera_floatball()
            self.sociushelper.stop_live()
            self.sociushelper.click_camera_floatball()
            self.sociushelper.record_ingame()
            self.sociushelper.click_camera_floatball()
            self.sociushelper.stop_live()

        except:
            self.logger.info('caught exception: {}'.format(sys.exc_info()[0]))
            self.syshelper.capture_screen("test_game")
            raise

