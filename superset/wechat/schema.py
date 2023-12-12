# -*- coding:utf-8 -*-
"""
@author:孟小征
@software:PyCharm
@file schema.py
@time 2023/12/12 21:23
"""

from marshmallow import Schema
from marshmallow.fields import String


class WechatLoginToQrcode(Schema):
    qrcode = String()
