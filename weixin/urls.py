# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import WeixinInterfaceView


urlpatterns = [
    url(r'', csrf_exempt(WeixinInterfaceView.as_view())),
]

