from time import time, sleep
from urllib import parse

import requests
import random
import hashlib, os
from wechat import WeChatAction
from configparser import ConfigParser
import logging
logging.basicConfig(level=logging.DEBUG, \
    format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',\
    filename="running.log",\
    filemode="a")
logger = logging.getLogger(__name__)

import sys
sys.path.append('..')

class Chatbot:
    def __init__(self, session, question):
        self.session = session
        self.question = question.replace(" ", "")
        self.time_stamp = str(int(time()))
        self.nonce_str = ''.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz', 10))
        self.params = {'app_id': '', 'session': self.session, 'question': self.question,
                       'time_stamp': self.time_stamp, 'nonce_str': self.nonce_str, 'sign': ''}
        self.config_file = "urlConfig.ini"
        # 读取参数配置文件
        conn = ConfigParser()
        if not os.path.exists(self.config_file):
             raise FileNotFoundError("%s not exists" % self.config_file)
        conn.read(self.config_file)
        self.appkey = conn.get("urlArgs","appkey")
        self.params['app_id'] = conn.get("urlArgs","app_id")
        
        # if os.path.exists(self.sign_file):
        #     with open(self.sign_file, "r") as f:
        #         self.params['sign'] = f.read()

    def getReqSign(self):
        t = []
        for key in sorted(self.params):
            value = parse.quote(str(self.params[key]))
            if value != "":
                t.append(key + "=" + value + "&")
        s = ''.join(t) + "app_key=" + self.appkey
        hash_md5 = hashlib.md5()
        hash_md5.update(s.encode())
        sign = hash_md5.hexdigest().upper()
        self.params['sign'] = sign
        # with open("sign.txt", "w") as f:
        #     f.write(sign)

    def doHttpPost(self):

        # self.getReqSign()
        url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"
        r = requests.post(url=url, data=self.params)
        r_content = eval(r.text)
        return r_content

def testChatbot():
    session = ''.join(random.sample('0123456789', 5))
    fuc = Chatbot(session, "你好呀")
    fuc.getReqSign()
    r_session = fuc.doHttpPost().get('data').get('session')
    r_answer = fuc.doHttpPost().get('data').get('answer')
    if fuc.doHttpPost().get('ret') == 0 and \
        fuc.doHttpPost().get('msg') == 'ok':
        print("会话ID：", r_session)
        logger.debug("msg ret: 0"+r_answer)
        print("reply: ", r_answer)
    else:
        print("参数错误，请重试")
    sleep(random.randint(2, 6))


if __name__ == '__main__':
    session = ''.join(random.sample('0123456789', 5))
    wt = WeChatAction()
    previoutMessage = ""
    while True:
        currentMessag = wt.get_message()
        if currentMessag == previoutMessage or currentMessag == "":
            sleep(random.randint(2, 6))
            continue
        print("message: ", currentMessag)
        fuc = Chatbot(session, currentMessag)
        fuc.getReqSign()
        r_session = fuc.doHttpPost().get('data').get('session')
        r_answer = fuc.doHttpPost().get('data').get('answer')
        if fuc.doHttpPost().get('ret') == 0 and \
            fuc.doHttpPost().get('msg') == 'ok':
            print("会话ID：", r_session)
            logger.debug("msg ret: 0"+r_answer)
            print("reply: ", r_answer)
            wt.send_txt(r_answer)
        else:
            print("参数错误，请重试")
        sleep(random.randint(2, 6))
    # testChatbot()
