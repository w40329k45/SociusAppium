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

from lib.syshelper import SysHelper
from lib.sociushelper import SociusHelper
from lib.accounthelper import AccountHelper
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

class DiscoveryAndSupportTests(BaseTests):
    """docstring for DiscoveryAndSupportTests"""
    def test_allpage(self):
        try:
            expectedDisplayName=config.EXISTING_FACEBOOK_ACCOUNT1_DISPLAYNAME
            expectedSoociiId=config.EXISTING_FACEBOOK_ACCOUNT1_SOOCIIID

            # Facebook Login button on Soocii
            self.sociushelper.click_facebook_login_button()
            self.syshelper.login_facebook_account(config.EXISTING_FACEBOOK_ACCOUNT1, config.EXISTING_FACEBOOK_ACCOUNT1_PWD)

            # confirm acquiring permission dialog
            self.sociushelper.click_require_permission_button()

            self.sociushelper.swipe_discover()

            # check newsfeedinfo
            self.assertTrue(self.sociushelper.get_newsfeed_info())

            #check aboutme
            self.assertTrue(self.sociushelper.check_aboutme(expectedDisplayName))

            #check support
            self.assertTrue(self.sociushelper.check_support())

            #check friendlist
            self.assertTrue(self.sociushelper.get_friendlist_info())

            self.sociushelper.swipe_to_fans()

            self.assertTrue(self.sociushelper.check_suggest())

            self.sociushelper.swipe_to_SearchId()
            self.sociushelper.get_idsearch("scheng1")
            self.sociushelper.go_back()
            self.sociushelper.swipe_discover()
            self.sociushelper.swipe_refresh()
        except:
            self.logger.info('caught exception: {}'.format(sys.exc_info()[0]))
            self.syshelper.capture_screen("test_allpage")
            raise

    def test_discoverytap(self):
        reload(sys)
        sys.setdefaultencoding("utf-8")
        try:
            self.sociushelper.click_login_by_email_link()
            self.sociushelper.login_account("channing@gmail.com", "zxasqw123")

            self.sociushelper.click_require_permission_button()

            self.sociushelper.swipe_discover()

            for x in range(10):
                self.sociushelper.swipe_loading()
                self.assertTrue(self.sociushelper.get_videocard())

            for y in range(15):
                self.sociushelper.swipe_refresh()

            self.sociushelper.click_onlinevideocard()

            self.sociushelper.click_videocard()

            self.sociushelper.swipe_refresh()
            self.sociushelper.swipe_refresh()

            self.sociushelper.check_hashtag()


        except Exception as e:
            self.logger.info('caught exception: {}'.format(sys.exc_info()[0]))
            self.syshelper.capture_screen("test_discoverytap")
            raise

    def test_zendesk(self):
        try:
            self.sociushelper.click_login_by_email_link()
            self.sociushelper.login_account("channing@gmail.com", "zxasqw123")

            self.sociushelper.click_require_permission_button()

            self.sociushelper.swipe_to_support()

            self.sociushelper.check_zendesk()

            self.sociushelper.check_faq()

            self.sociushelper.check_contact("ignore this ! automation test!")
        except Exception as e:
            self.logger.info('caught exception: {}'.format(sys.exc_info()[0]))
            self.syshelper.capture_screen("test_zendesk")
            raise

