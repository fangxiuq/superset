# -*- coding:utf-8 -*-
"""
@author:孟小征
@software:PyCharm
@file wechat_api.py
@time 2023/12/11 09:45
"""

import json
import logging
import os
from random import sample
from string import ascii_letters, digits
import time
import uuid
from flask_appbuilder.api import expose
from flask import jsonify, request

from wechatpayv3 import WeChatPay, WeChatPayType

# 微信支付商户号（直连模式）或服务商商户号（服务商模式，即sp_mchid)
MCHID = '1234567890'

# 商户证书私钥
with open('path_to_key/apiclient_key.pem') as f:
    PRIVATE_KEY = f.read()

# 商户证书序列号
CERT_SERIAL_NO = '444F4864EA9B34415...'

# API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
APIV3_KEY = 'MIIEvwIBADANBgkqhkiG9w0BAQE...'

# APPID，应用ID或服务商模式下的sp_appid
APPID = 'wxd678efh567hg6787'

# 回调地址，也可以在调用接口的时候覆盖
NOTIFY_URL = 'https://www.xxxx.com/notify'

# 微信支付平台证书缓存目录，减少证书下载调用次数，首次使用确保此目录为空目录.
# 初始调试时可不设置，调试通过后再设置，示例值:'./cert'
CERT_DIR = None

# 日志记录器，记录web请求和回调细节
logging.basicConfig(filename=os.path.join(os.getcwd(), 'demo.log'), level=logging.DEBUG,
                    filemode='a',
                    format='%(asctime)s - %(process)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger("demo")

# 接入模式:False=直连商户模式，True=服务商模式
PARTNER_MODE = False

PROXY = None

# 初始化
wxpay = WeChatPay(
    wechatpay_type=WeChatPayType.NATIVE,
    mchid=MCHID,
    private_key=PRIVATE_KEY,
    cert_serial_no=CERT_SERIAL_NO,
    apiv3_key=APIV3_KEY,
    appid=APPID,
    notify_url=NOTIFY_URL,
    cert_dir=CERT_DIR,
    logger=LOGGER,
    partner_mode=PARTNER_MODE,
    proxy=PROXY)


def native_pay(out_trade_no, description, amount):
    # 下单成功后即可获取到'code_url'，将'code_url'转换为二维码，并用微信扫码即可进行支付测试。
    # out_trade_no = '1231112312'
    # description = 'test-description'
    # amount = 1
    code, message = wxpay.pay(
        description=description,
        out_trade_no=out_trade_no,
        amount={'total': amount},
        pay_type=WeChatPayType.NATIVE
    )
    return jsonify({'code': code, 'message': message})


@expose("/pay/wechat/notify", methods=("POST",))
def notify():
    result = wxpay.callback(request.headers, request.data)
    if result and result.get('event_type') == 'TRANSACTION.SUCCESS':
        resp = result.get('resource')
        appid = resp.get('appid')
        mchid = resp.get('mchid')
        out_trade_no = resp.get('out_trade_no')
        transaction_id = resp.get('transaction_id')
        trade_type = resp.get('trade_type')
        trade_state = resp.get('trade_state')
        trade_state_desc = resp.get('trade_state_desc')
        bank_type = resp.get('bank_type')
        attach = resp.get('attach')
        success_time = resp.get('success_time')
        payer = resp.get('payer')
        amount = resp.get('amount').get('total')
        # TODO: 根据返回参数进行必要的业务处理，处理完后返回200或204
        return jsonify({'code': 'SUCCESS', 'message': '成功'})
    else:
        return jsonify({'code': 'FAILED', 'message': '失败'}), 500
