# -*- coding: utf-8 -*-f
import xml.etree.ElementTree as ET
import time
import urllib.request
import json


def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    xmlData = ET.fromstring(web_data)
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(xmlData)


class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text


class TextMsg(Msg):
    def __init__(self, xmlData):
        super().__init__(xmlData)
        self.Content = xmlData.find('Content').text
        self.dict = dict()
        self.dict['ToUserName'] = self.FromUserName
        self.dict['FromUserName'] = self.ToUserName
        self.dict['CreateTime'] = int(time.time())
        self.dict['Content'] = self.Content


class Base(object):
    def __init__(self):
        self.__appSecret = '7677d9558ea17b392f46b8b0b919e28c'
        self.__AppID = 'wx34944ee42a97682a'
        self.__leftTime = 0

    def __real_get_access_token(self):
        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
                   "client_credential&appid=%s&secret=%s" % (self.__AppID, self.__appSecret))
        urlResp  = urllib.request.urlopen(postUrl)
        urlResp = json.loads(urlResp.read().decode('utf-8'))
        self.__accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']

    def get_acess_token(self):
        if self.__leftTime < 10:
            self.__real_get_access_token()
        return self.__accessToken

    def run(self):
        while True:
            if self.__leftTime > 10:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                self.__real_get_access_token()


class Menu(object):
    def __init__(self):
        pass

    def create(self, postData, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        if isinstance(postData, str):
            postData = postData.encode('utf-8')
        urlResp = urllib.request.urlopen(url=postUrl, data=postData)
        print(urlResp.read())


    def query(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % accessToken
        urlResp = urllib.request.urlopen(url=postUrl)
        print(urlResp.read())

    def delete(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % accessToken
        urlResp = urllib.request.urlopen(url=postUrl)
        print(urlResp.read())

    def get_current_selfmenu_info(self, accessToken):
       postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
       urlResp = urllib.request.urlopen(url=postUrl)
       print(urlResp.read())

if __name__ == '__main__':
    myMenu = Menu()
    postJson = """
    {
        "button":
        [
            {
                "type": "click",
                "name": "成语接龙",
                "key":  "cyjl"
            },
            {
                "name": "公众平台",
                "sub_button":
                [
                    {
                        "type": "view",
                        "name": "更新公告",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                    },
                    {
                        "type": "view",
                        "name": "接口权限说明",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                    },
                    {
                        "type": "view",
                        "name": "返回码说明",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433747234&token=&lang=zh_CN"
                    }
                ]
            }
          ]
    }
    """
    accessToken = Base().get_acess_token()
    print(accessToken)
    myMenu.create(postJson, accessToken)


