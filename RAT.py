#coding=utf-8
import os
import re
import sys
import pytest
import logging
import unittest
import subprocess

from appium import webdriver

import config
from lib.syshelper import SysHelper
from lib.sociushelper import SociusHelper
from lib.accounthelper import AccountHelper

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

# logger
logger = logging.getLogger()
logFormatter = logging.Formatter(
    '[%(asctime)-15s][%(filename)s][%(funcName)s#%(lineno)d] %(message)s')
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(logFormatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

def getDeviceProp(prop):
    p1 = subprocess.Popen(['adb', 'shell', 'getprop'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', prop], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    line = p2.communicate()[0]
    # parse value
    p = re.compile('\[ro.{}\]: \[(.+)\]'.format(prop))
    return p.findall(line)[0]

class BaseTests(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = getDeviceProp('build.version.release')
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['unicodeKeyboard'] = True
        desired_caps['resetKeyboard'] = True
        #desired_caps['full-reset'] = True
        desired_caps['app'] = PATH(
            config.PATH_TO_TEST_APK
        )

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(5)
        self.logger = logging.getLogger()

        self.syshelper = SysHelper(self.driver, desired_caps['platformName'], desired_caps['platformVersion'])
        self.sociushelper = SociusHelper(self.driver, desired_caps['platformName'], desired_caps['platformVersion'])

    def tearDown(self):
        # TODO: reset keyboard

        # remove app
        self.driver.close_app()

        # end the session
        self.driver.quit()

class FacebookAccountTests(BaseTests):
    # Login with existing facebook account and enable usage access once
    @pytest.mark.first
    def test_fresh_install_and_enable_usage_access(self):
        try:
            expectedDisplayName=config.EXISTING_FACEBOOK_ACCOUNT1_DISPLAYNAME
            expectedSoociiId=config.EXISTING_FACEBOOK_ACCOUNT1_SOOCIIID

            # Facebook Login button on Soocii
            self.sociushelper.click_facebook_login_button()
            self.syshelper.login_facebook_account(config.EXISTING_FACEBOOK_ACCOUNT1, config.EXISTING_FACEBOOK_ACCOUNT1_PWD)

            # confirm acquiring permission dialog
            self.sociushelper.click_require_permission_button()

            # only need to skip floating ball guide mark once
            self.sociushelper.skip_floating_ball_guide_mark()

            # only need to enable usage access once
            self.syshelper.enable_usage_access()

            # only need to enable draw on top layer once
            self.syshelper.enable_draw_on_top_layer()

            # expect seeing discover page
            self.assertTrue(self.sociushelper.is_discover())
            displayName, soociiId = self.sociushelper.get_personal_info()
            self.assertTrue(expectedDisplayName==displayName,
                u"expect value {}, but return unexpected {}".format(expectedDisplayName, displayName))
            self.assertTrue(expectedSoociiId==soociiId,
                u"expect value {}, but return unexpected {}".format(expectedSoociiId, soociiId))

            # switch to home and back to soocii
            self.syshelper.press_home_key()
            self.syshelper.start_soocii()
            displayName, soociiId = self.sociushelper.get_personal_info()
            self.assertTrue(expectedDisplayName==displayName,
                u"expect value {}, but return unexpected {}".format(expectedDisplayName, displayName))
            self.assertTrue(expectedSoociiId==soociiId,
                u"expect value {}, but return unexpected {}".format(expectedSoociiId, soociiId))
            # don't delete the account
        except:
            self.logger.info('caught exception: {}'.format(sys.exc_info()[0]))
            self.syshelper.capture_screen("test_fresh_install_and_enable_usage_access")
            raise

    # Login with new facebook account who friend with existing facebook/soocii account
    def test_login_new_facebook_account(self):
        try:
            expectedDisplayName=config.NEW_FACEBOOK_ACCOUNT1_DISPLAYNAME
            expectedSoociiId=config.NEW_FACEBOOK_ACCOUNT1_SOOCIIID

            # Facebook Login button on Soocii
            self.sociushelper.click_facebook_login_button()
            self.syshelper.login_facebook_account(config.NEW_FACEBOOK_ACCOUNT1, config.NEW_FACEBOOK_ACCOUNT1_PWD)

            # flow to create new account
            self.sociushelper.create_account(expectedDisplayName, expectedSoociiId)
            self.sociushelper.add_followers()

            # confirm acquiring permission dialog
            self.sociushelper.click_require_permission_button()

            # expect seeing discover page
            self.assertTrue(self.sociushelper.is_discover())
            displayName, soociiId = self.sociushelper.get_personal_info()
            self.assertTrue(expectedDisplayName==displayName,
                u"expect value {}, but return unexpected {}".format(expectedDisplayName, displayName))
            self.assertTrue(expectedSoociiId==soociiId,
                u"expect value {}, but return unexpected {}".format(expectedSoociiId, soociiId))

            # switch to home and back to soocii
            self.syshelper.press_home_key()
            self.syshelper.start_soocii()
            displayName, soociiId = self.sociushelper.get_personal_info()
            self.assertTrue(expectedDisplayName==displayName,
                u"expect value {}, but return unexpected {}".format(expectedDisplayName, displayName))
            self.assertTrue(expectedSoociiId==soociiId,
                u"expect value {}, but return unexpected {}".format(expectedSoociiId, soociiId))
        except:
            self.logger.info('caught exception: {}'.format(sys.exc_info()[0]))
            self.syshelper.capture_screen("test_login_new_facebook_account")
            raise
        finally:
            # delete the account for next time
            self.sociushelper.click_delete_account_button()

    # TODO: Login with new facebook account who does NOT friend with any facebook/soocii account

class EmailAccountTests(BaseTests):
    # Login with new email account
    def test_login_new_email_account(self):
        try:
            accounthelper = AccountHelper()

            # Create new account button on Soocii
            self.sociushelper.click_create_new_account_using_email_button()

            # flow to create new account
            self.sociushelper.create_account(
                accounthelper.name,
                accounthelper.name,
                accounthelper.email,
                "password1234")

            # confirm acquiring permission dialog
            self.sociushelper.click_require_permission_button()

            # expect seeing discover page
            self.assertTrue(self.sociushelper.is_discover())
            displayName, soociiId = self.sociushelper.get_personal_info()
            self.assertTrue(accounthelper.name==displayName,
                            u"expect value {}, but return unexpected {}".format(accounthelper.name, displayName))
            self.assertTrue(accounthelper.name==soociiId,
                            u"expect value {}, but return unexpected {}".format(accounthelper.name, soociiId))

            # switch to home and back to soocii
            self.syshelper.press_home_key()
            self.syshelper.start_soocii()
            displayName, soociiId = self.sociushelper.get_personal_info()
            self.assertTrue(accounthelper.name==displayName,
                            u"expect value {}, but return unexpected {}".format(accounthelper.name, displayName))
            self.assertTrue(accounthelper.name==soociiId,
                            u"expect value {}, but return unexpected {}".format(accounthelper.name, soociiId))
        except:
            self.logger.info('caught exception: {}'.format(sys.exc_info()[0]))
            self.syshelper.capture_screen("test_login_new_email_account")
            raise
        finally:
            # delete the account for next time
            self.sociushelper.click_delete_account_button()

    # Login with existing email account
    def test_login_existing_email_account(self):
        try:
            accounthelper = AccountHelper()

            # Create new account button on Soocii
            self.sociushelper.click_create_new_account_using_email_button()

            # flow to create new account
            self.sociushelper.create_account(
                accounthelper.name,
                accounthelper.name,
                accounthelper.email,
                "password1234")

            # confirm acquiring permission dialog
            self.sociushelper.click_require_permission_button()

            # expect seeing discover page
            self.assertTrue(self.sociushelper.is_discover())

            # logout
            self.sociushelper.click_logout_button()

            # login with the same account again
            self.sociushelper.click_login_by_email_link()
            self.sociushelper.login_account(accounthelper.email, "password1234")

            # expect seeing discover page
            self.assertTrue(self.sociushelper.is_discover())
            displayName, soociiId = self.sociushelper.get_personal_info()
            self.assertTrue(accounthelper.name==displayName,
                            u"expect value {}, but return unexpected {}".format(accounthelper.name, displayName))
            self.assertTrue(accounthelper.name==soociiId,
                            u"expect value {}, but return unexpected {}".format(accounthelper.name, soociiId))

            # switch to home and back to soocii
            self.syshelper.press_home_key()
            self.syshelper.start_soocii()
            displayName, soociiId = self.sociushelper.get_personal_info()
            self.assertTrue(accounthelper.name==displayName,
                            u"expect value {}, but return unexpected {}".format(accounthelper.name, displayName))
            self.assertTrue(accounthelper.name==soociiId,
                            u"expect value {}, but return unexpected {}".format(accounthelper.name, soociiId))
        except:
            self.logger.info('caught exception: {}'.format(sys.exc_info()[0]))
            self.syshelper.capture_screen("test_login_existing_email_account")
            raise
        finally:
            # delete the account for next time
            self.sociushelper.click_delete_account_button()

    # TODO: create existing email account

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
            self.sociushelper.get_idsearch()
            self.sociushelper.swipe_discover()
            self.sociushelper.swipe_refresh()
        except:
            self.logger.info('caught exception: {}'.format(sys.exc_info()[0]))
            self.syshelper.capture_screen("test_login_existing_email_account")
            raise
            
    def test_discoverytap(self):
        try:
            expectedDisplayName=config.EXISTING_FACEBOOK_ACCOUNT1_DISPLAYNAME
            expectedSoociiId=config.EXISTING_FACEBOOK_ACCOUNT1_SOOCIIID

            # Facebook Login button on Soocii
            self.sociushelper.click_facebook_login_button()
            self.syshelper.login_facebook_account(config.EXISTING_FACEBOOK_ACCOUNT1, config.EXISTING_FACEBOOK_ACCOUNT1_PWD)

            # confirm acquiring permission dialog
            self.sociushelper.click_require_permission_button()

            self.sociushelper.swipe_discover()

            for x in range(5):
                self.sociushelper.swipe_loading()
                self.assertTrue(self.sociushelper.get_videocard())

            for y in range(6):
                self.sociushelper.swipe_refresh()

            self.sociushelper.click_onlinevideocard()

            self.sociushelper.click_videocard()

            self.sociushelper.swipe_refresh()
            self.sociushelper.swipe_refresh()

            self.sociushelper.check_hashtag()
            

        except Exception as e:
            raise

    def test_zendesk(self):
        try:
            expectedDisplayName=config.EXISTING_FACEBOOK_ACCOUNT1_DISPLAYNAME
            expectedSoociiId=config.EXISTING_FACEBOOK_ACCOUNT1_SOOCIIID

            # Facebook Login button on Soocii
            self.sociushelper.click_facebook_login_button()
            self.syshelper.login_facebook_account(config.EXISTING_FACEBOOK_ACCOUNT1, config.EXISTING_FACEBOOK_ACCOUNT1_PWD)

            # confirm acquiring permission dialog
            self.sociushelper.click_require_permission_button()

            self.sociushelper.swipe_to_support()

            self.sociushelper.check_zendesk()

            self.sociushelper.check_faq()

            self.sociushelper.check_contact()
        except Exception as e:
            raise
