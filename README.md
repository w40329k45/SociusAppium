# Appium for Socius

群攜科技 [Soocii App](https://play.google.com/store/apps/details?id=me.soocii.socius&hl=zh_TW) 自動化測試

## 環境

* [Android Studio 2.0](https://developer.android.com/studio/index.html)
* Python 2.7
    * pip 9.0.1
    * pip install -r requirement.txt
* [Appium](http://appium.io/)
* [Android File Transfer](https://www.android.com/filetransfer/)
* OSX 環境變數

```shell
export ANDROID_HVPROTO=ddm
export JAVA_HOME="$(/usr/libexec/java_home -v 1.8)"
export ANDROID_HOME=/Users/jonas/Library/Android/sdk/
export PATH="$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$JAVA_HOME/bin"
```

## 工具

* Uiautomatorviewer
    * a tool to inspect app resource id, class name, text
    * (OSX) ~/Library/Android/sdk/tools/

* Appium Inspector
    * a tool to inspect app resource id, class name, text and xpath

## 執行

* 將 config.py 複製至 Readme.md 相同路徑

以下是範例，請接洽主管取得此設定檔

```python
#coding=utf-8

# Test environment
PLATFORM_VERION='6.0.1'
#PLATFORM_VERION='5.0'
PATH_TO_TEST_APK='soocii_xxx_staging.apk'

# Login with existing account and enable usage access once
EXISTING_FACEBOOK_ACCOUNT1="test1@gmail.com"
EXISTING_FACEBOOK_ACCOUNT1_PWD="test1"
EXISTING_FACEBOOK_ACCOUNT1_DISPLAYNAME=u"錢多多"
EXISTING_FACEBOOK_ACCOUNT1_SOOCIIID="test1.mobi"

# Login with new facebook account who friend with existing facebook account
NEW_FACEBOOK_ACCOUNT1="test2@gmail.com"
NEW_FACEBOOK_ACCOUNT1_PWD="test2"
NEW_FACEBOOK_ACCOUNT1_DISPLAYNAME="SoociiQA"
NEW_FACEBOOK_ACCOUNT1_SOOCIIID="test2.qa1"
```

* 將測試的 APK 檔複製至 Readme.md 相同路徑，並記得修改 config.py

```python
PATH_TO_TEST_APK='soocii_xxx_staging.apk'
```

* 透過 USB 連接 Android 裝置
    * Use ```adb devices``` to make sure the device is connected

* 執行測項

```shell
# all test cases
py.test -x RAT.py
# single test case
py.test -x RAT.py::SociusTests::test_login_new_facebook_account
```
