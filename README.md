# Python3 与 uiautomator2 的微信小工具。

## 设计架构
* uiautomator2负责图形界面操作
* easyorc是开源的OCR识别库，负责识别图片文字。目前效果比tesseract好，但是对环境要求比tesseract高。tesseract识别文字，准确率勉强够用，有时出现文字识别为空
* requests请求调用腾讯ai接口
## 环境要求
* python3
* python3所需要安装的库
    - easyorc
    - requests
    - uiautomator2
    - pillow

## 安装步骤
1. 配置环境
```sh
pip install -U uiautomator2 pillow && python -m uiautomator2 init 
(python -m uiautomator2 init –mirror这是国内的，比较快)
```
2. 获取腾讯ai请求参数的
将获取的app_id, appkey填写在urlConfig.ini.template
```ini
;腾讯ai机器人请求参数
[urlArgs]
app_id=
appkey=
```
删去文件名结尾的.template,修改为urlConfig.ini
3. 手机屏幕切换到微信用户聊天界面

linux
```
chmod +x run.sh
./run.sh
```
windows
```
.\run.bat
```
## 运行说明
* 目前只支持android设备，ios理论上也是可以通过tidevice+WebDriverAgent实现的。
但是本人与周围人没有能运行Xcode的Mac设备，无法给ios安装WebDriverAgent，所以无法进行ios设备的开发。除非有人愿意贡献一下。
* 运行时手机屏幕必须一直在微信聊天界面，否则程序运行会出现问题。
* 分屏模式理论上只要有微信聊天界面即可。

刚启动会根据手机屏幕，如果显示对方发出的消息你一直未回答，则自动作出答复
* 目前无法提取表情包组件
以下的答复腾讯机器人无法作出反映:
 * "机器人怎么会说话"


## 未来展望
目前项目还是具备最基本的功能，未来开发中会增加更多微信界面的自动化管理，增加更多的请求接口，比如访问天气和增加其他的聊天机器人调用接口，向sfyc23/EverydayWechat项目靠进。针对ios设备，真的需要一台能运行Xcode的苹果电脑才行，本人已经试过很多办法包括virtualbox运行MacOS虚拟机，但是没有一个成功的。

感谢项目:
https://github.com/sfyc23/EverydayWechat