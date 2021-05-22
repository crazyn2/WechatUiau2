## 设计架构
* tesseract识别文字，准确率勉强够用，有时出现文字识别为空
* easyorc开源的OCR识别库，目前效果比tesseract好，但是对环境要求比tesseract高
## 环境要求
* python3
* python3所需要安装的库
    - easyorc
    - requests
    - uiautomator2

## 运行说明
刚启动会根据手机屏幕，如果显示对方发出的消息你一直未回答，则自动作出答复
* 目前无法提取表情包组件
以下的答复腾讯机器人无法作出反映:
 * "机器人怎么会说话"