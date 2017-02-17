# -*- coding: utf-8 -*-
import hashlib
import time
from lxml import etree
from django.views.generic.base import View
from django.shortcuts import render

from .weixinTools import parse_xml


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

        if recMsg.Content == "help":
            recMsg.dict['Content'] = '1、直接回复，学你说话\n2、回复 cy+成语，玩成语接成'
        else:
            recMsg.dict['Content'] = ''.join(['我现在只能学你说话:', recMsg.Content,
                           '\n反过来说也行:', recMsg.Content[::-1]])
        return render(request, 'reply_text.xml',
                      recMsg.dict, content_type='application/xml'
                      )
