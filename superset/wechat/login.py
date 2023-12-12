# -*- coding:utf-8 -*-
"""
@author:孟小征
@software:PyCharm
@file login.py
@time 2023/12/12 20:19
"""
import time
import hashlib
import requests
from lxml import etree
from flask import g, Response
from superset.views.base_api import BaseSupersetApi
from superset.wechat.appKeys import APPID
from superset.wechat.schema import WechatLoginToQrcode
from flask_appbuilder.api import expose, safe

qrcode_response_schema = WechatLoginToQrcode()


class WechatLoginRestApi(BaseSupersetApi):
    resource_name = "wechat"
    openapi_spec_tag = "WechatLoginRestApi"
    openapi_spec_component_schemas = (WechatLoginToQrcode,)

    # 获取二维码
    @expose("/login/qrcode", methods=("GET",))
    def loginToQrcode(self) -> Response:
        t = time.time()
        h = hashlib.md5()
        h.update(str(t).encode(encoding='utf-8'))
        state = h.hexdigest()
        # 扫描后给微信的重定向url地址（这个地址会携带code与state）
        redirectUrl = "127.0.0.1:8000/api/weChatLogin"

        url = f'https://open.wechat.qq.com/connect/qrconnect?appid={APPID}&redirect_uri={redirectUrl}&response_type=code' \
              f'&scope=snsapi_login&state={state}#wechat_redirect'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                html = etree.HTML(response.text)
                img = html.xpath('//div[@class="wrp_code"]/img[1]/@src')
                qrcode = "https://open.weChat.qq.com" + img[0]
            else:
                qrcode = ''
        except Exception as e:
            qrcode = ''

        return self.response(200, result={'qrcode': qrcode})
