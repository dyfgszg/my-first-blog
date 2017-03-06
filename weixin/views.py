# -*- coding: utf-8 -*-
import hashlib
import sqlite3
import time
import datetime
import random
from lxml import etree
from django.views.generic.base import View
from django.shortcuts import render

from .weixinTools import parse_xml

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class WeixinInterfaceView(View):
    def get(self, request):
        # 得到GET内容
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        # 自己的token
        # 这里改写你在微信公众平台里输入的token
        token = 'ddggzxyzdy520'
        # 字典序排序
        tmpList = [token, timestamp, nonce]
        tmpList.sort()
        tmpstr = '%s%s%s' % tuple(tmpList)
        # sha1加密算法
        tmpstr = hashlib.sha1(tmpstr.encode('utf-8')).hexdigest()

        # 如果是来自微信的请求，则回复echostr
        if tmpstr == signature:
            return render(request, 'get.html', {'str': echostr},
                          content_type='text/plain')

    def post(self, request):
        str_xml = request.body.decode('utf-8')  # use body to get raw data
        recMsg = parse_xml(str_xml)
        re_content = recMsg.Content.split("+", 1)
        manage_key = re_content[0]
        manage_list = {
            'xs': self.xue_she,
            'cy': self.cy_jielong,
        }
        manage = manage_list.get(manage_key, self.re_help)
        try:
            recMsg.dict['Content'] = manage(re_content[1])
        except IndexError:
            recMsg.dict['Content'] = manage(re_content[0])
        return render(request, 'reply_text.xml',
                      recMsg.dict, content_type='application/xml'
                      )

    def re_help(self, content_txt):
        return '1、回复xs+文字：学你说话:)\n2、回复 cy+成语：玩成语接龙'

    def xue_she(self, content_txt):
        return ''.join(['我现在只能学你说话:', content_txt,
                        '\n反过来说也行:', content_txt[::-1]])

    def cy_jielong(self, content_txt):

        def get_input_word(input_word):
            first_word = content_txt[len(input_word) - 1:len(input_word)]
            return first_word

        def get_result_by_input(input_word):
            random.seed(datetime.datetime.now())
            conn = sqlite3.connect(os.path.join(BASE_DIR, 'cnzz.db'))
            cursor = conn.cursor()
            print(cursor)
            cursor.execute('select ChengYU, DianGu from YesoulChenYu where ChengYu like "' + input_word + '%";')
            res = cursor.fetchall()
            res = res[random.randint(0, len(res) - 1)]
            res = '-典故:'.join(res)
            cursor.close()
            conn.close()
            return res

        input_word = content_txt
        first_word = get_input_word(input_word)
        return get_result_by_input(first_word)
