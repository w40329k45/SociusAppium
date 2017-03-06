# Appium for Socius

群攜科技 [Soocii App](https://play.google.com/store/apps/details?id=me.soocii.socius&hl=zh_TW) 自動化測試

## 環境

* [Android Studio 2.0](https://developer.android.com/studio/index.html)
* Python 2.7
    * pip 9.0.1
    * pip install -r requirement.txt
* [Appium](http://appium.io/)
* Environment Variables (OSX)

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

* Connect Android device thru. USB
* Use ```adb devices``` to make sure the device is connected
* Run tests

```shell
# all test cases
py.test -x RAT.py
# single test case
py.test -x RAT.py::SociusTests::test_login_new_facebook_account
```