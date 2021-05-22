import uiautomator2 as u2
# import pytesseract
import re
from PIL import Image
import easyocr
import numpy as np
# d = u2.connect()
# d_width, d_height = d.window_size()
# d_width_center = d_width / 2

class WeChatAction():
    '''
    __init__
    :param: uuid: the uuid of the target devices
    '''
    def __init__(self, uuid=None):
        if uuid == None:
            self.d = u2.connect()
        else:
            self.d = u2.connect(uuid)
        d_width, _ = self.d.window_size()
        self.d_width_center = d_width / 2
        self.reader = easyocr.Reader(['ch_sim','en'], gpu = False)

    def back(self):
        self.d.xpath('//*[@resource-id="com.tencent.mm:id/bjn"]/android.widget.LinearLayout[1]').click()




    def open_session(self):
        self.d.xpath('//*[@resource-id="com.tencent.mm:id/f67"] \
            /android.widget.LinearLayout[1]/android.widget.LinearLayout[1]').click()


    def get_text(self):
        
        '''
        elem: 
        info 输出所有变量内容
        text 文本内容
        '''
        
        for elem in self.d.xpath('//android.widget.TextView').all():
                print("element:",elem.text)

        # elements = d.xpath('//*[@resource-id="com.tencent.mm:id/awv"]/android.widget.RelativeLayout[2]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]').all()
        # for ele in elements:
        #     children = ele.elem.getchildren()
        #     for child in children:
                
        #         for key in child.keys():
        #             print(key,":",child.get(key))
        #         grandchildren = child.getchildren()
        #         for grandchild in grandchildren:
        #             print(grandchild.keys())

    def send_txt(self, text):
        '''
        :param text: the string you want to send
        '''
        # 如果内容为空，是无法发送的
        input_ele = self.d(resourceId="com.tencent.mm:id/iki")
        if text=="" or not input_ele.exists():
            return
        
        input_ele.click()
        self.d.set_fastinput_ime(True)
        self.d(resourceId="com.tencent.mm:id/iki").set_text(text)
        self.d.send_keys(text)
        self.d(resourceId="com.tencent.mm:id/ay5").click()
        # self.d.set_fastinput_ime(False)
        # self.d.xpath('//*[@resource-id="com.tencent.mm:id/awv"]/android.widget.RelativeLayout[*]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]').all()[0].click()
        # d.set_fastinput_ime(True)

    # 先截屏，再裁剪文字区域，tesseract文字识别
    def get_message(self):
        '''
        get the visual messages in the current screen whitch is split
        by the device owner sent
        '''
        message = ""
        elements = self.d.xpath('//*[@resource-id="com.tencent.mm:id/awv"]/android.widget.RelativeLayout[*]/android.widget.LinearLayout[1]/android.widget.LinearLayout[1]').all()
        message_list = [[]]
        index = 0
        check = 0
        i = 0
        for ele in elements:
            '''
            ele.screenshot() return: PIL.Image
            '''
            image = ele.screenshot()
            i += 1
            # image.save("m%d.png" % i)
            parent = ele.parent()

            # filter the message widget components
            # the index of message widget is sometimes 0 or 1.
            for peer in parent.elem.getchildren():

                if peer.get("resource-id") != "":
                    # unfortunately the returned type of .get() is string 
                    string = peer.get("bounds")
                    nums = re.findall(r"\d+\.?\d*",string)
                    # check the head portrait position in screen 
                    if(int(nums[0]) < self.d_width_center):
                        
                        check = 0
                        message_list[index].append(image)
                        # image.save("if%d.png" % i)
                        # print(pytesseract.image_to_string(image,\
                            # lang="chi_sim").rstrip())
                        # message += pytesseract.image_to_string(image,\
                        #     lang="chi_sim").\
                        #     rstrip().replace('\n', ' ').\
                        #     replace('\r', ' ') + " "
                    else:
                        if check == 0:
                            message_list.append([])
                            index += 1
                            check = 1
        # he/she didn't respond
        # if check == 1:
        #     return ""
        j = 0
        for img in message_list[-1]:
            # img.save("img%d.png" % j)
            j += 1
            # message += pytesseract.image_to_string(img,\
            #                 lang="chi_sim").\
            #                 rstrip().replace('\n', ' ').\
            #                 replace('\r', ' ') + " "
            lines = ""
            for each in self.reader.readtext(np.array(img), detail = 0):
                
                lines += each.rstrip()
            message += lines + " "
        return message

    def test(self):
        elements = self.d.xpath('//*[@resource-id="com.tencent.mm:id/awv"]/android.widget.RelativeLayout[*]//android.widget.ImageView').all()
        i = 0
        for ele in elements:
            # ele.xpath('//android.widget.ImageView')
            ele.screenshot().save("test%d.png"%i)
            i+=1
        


if __name__ == "__main__":
    

    # test()
    wt = WeChatAction()
    wt.test()
    



















