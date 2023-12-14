# -*- coding:utf-8 -*-
"""
@author:孟小征
@software:PyCharm
@file util.py
@time 2023/12/13 22:21
"""
import json

import requests


def weChatRequest(url, encoding="urf-8"):
    try:
        response = requests.get(url)
        response.encoding = encoding
        if response.status_code == 200: return response.json()
    except json.JSONDecodeError:
        return {}
