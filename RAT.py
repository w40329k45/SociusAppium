#coding=utf-8
import os
import sys
import logging
import pytest
import unittest

from appium import webdriver

import config
from lib.syshelper import SysHelper
from lib.sociushelper import SociusHelper

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

class SociusTests(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0.1'
        desired_caps['deviceName'] = 'Android Emulator'
        #desired_caps['full-reset'] = True
        desired_caps['app'] = PATH(
            'soocii_v0.0.1035_google_2017_0301_1102_staging.apk'
        )

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(5)
        self.logger = logging.getLogger()
        
        self.syshelper = SysHelper(self.driver)
        self.sociushelper = SociusHelper(self.driver)

    def tearDown(self):
        # remove app
        self.driver.close_app()

        # end the session
        self.driver.quit()

    # Login with existing facebook account and enable usage access once
    @pytest.mark.first
    def test_fresh_install_and_enable_usage_access(self):
        try:
            expectedDisplayName=config.EXISTING_FACEBOOK_ACCOUNT1_DISPLAYNAME
            expectedSoociiId=config.EXISTING_FACEBOOK_ACCOUNT1_SOOCIIID
            # Facebook Login button on Soocii
            self.sociushelper.click_facebook_login_button()

            self.syshelper.login_facebook_account(config.EXISTING_FACEBOOK_ACCOUNT1, config.EXISTING_FACEBOOK_ACCOUNT1_PWD)
            self.syshelper.allow_system_permissions()
            # only need to enable usage access once
            self.syshelper.enable_usage_access()
            self.sociushelper.skip_guide_mark()
            # expect seeing newsfeed page
            self.assertTrue(self.sociushelper.is_newsfeed())
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
            self.logger.info('caught exception: {}'.format(str(e)))
            self.syshelper.capture_screen("test_fresh_install_and_enable_usage_access")
            raise

    # Login with new facebook account who friend with existing facebook account
    def test_login_new_facebook_account(self):
        try:
            expectedDisplayName=config.NEW_FACEBOOK_ACCOUNT1_DISPLAYNAME
            expectedSoociiId=config.NEW_FACEBOOK_ACCOUNT1_SOOCIIID

            # Facebook Login button on Soocii
            self.sociushelper.click_facebook_login_button()

            self.syshelper.login_facebook_account(config.NEW_FACEBOOK_ACCOUNT1, config.NEW_FACEBOOK_ACCOUNT1_PWD)
            self.sociushelper.create_account(config.NEW_FACEBOOK_ACCOUNT1_DISPLAYNAME, config.NEW_FACEBOOK_ACCOUNT1_SOOCIIID)
            self.sociushelper.add_followers()
            self.syshelper.allow_system_permissions()
            self.sociushelper.skip_guide_mark()
            # expect seeing newsfeed page
            self.assertTrue(self.sociushelper.is_newsfeed())
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
            self.logger.info('caught exception: {}'.format(str(e)))
            self.syshelper.capture_screen("test_login_new_facebook_account")
            raise
        finally:
            # delete the account for next time
            self.sociushelper.click_delete_account_button()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SociusTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

