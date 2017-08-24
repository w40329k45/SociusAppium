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


def getDeviceProp(prop):
    p1 = subprocess.Popen(['adb', 'shell', 'getprop'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', prop], stdin=p1.stdout, stdout=subprocess.PIPE)

    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    line = p2.communicate()[0]
    # parse value
    p = re.compile('\[ro.{}\]: \[(.+)\]'.format(prop))
    return p.findall(line)[0]


#putout testfile
def nofile():
    subprocess.Popen(['adb', 'shell', 'rm', '/sdcard/Soocii/*.mp4', '/sdcard/soocii/*.jpeg'])

#putin testfile
def havefile():
    subprocess.Popen(['adb', 'push', os.path.abspath(path1)+"/.", '/sdcard/Soocii/'])
    print os.path.abspath(path1)+"/."

def opensnakeoff():
    subprocess.Popen(['adb', 'shell','monkey', '-p','com.wepie.snakeoff' ,'-c', 'android.intent.category.LAUNCHER 1'])
def opensoocii():
    subprocess.Popen(['adb', 'shell','monkey', '-p','me.soocii.socius.staging' ,'-c', 'android.intent.category.LAUNCHER 1'])


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


