import requests
import time
import hashlib
import hmac
import base64
import re
from urllib import parse


def SendMessage(message, send_address, send_password):

    # secret：密钥，机器人安全设置页面，加签一栏下面显示的SEC开头的字符串，例如：SECxxxxxxxx
    # secret = 'SEC2557de4136804caf94acf5a86e632e95145f94ca7a57ae92cbd15c0a1bbfa4b0'
    secret = send_password
    # access_token：创建完钉钉机器人之后会自动生成，例如：access_tokenxxxx
    # access_token = 'dff4d7ffc16f364f2380335c5850c179d283824918b87b931a90f345662e2bad'
    access_token = send_address
    # timestamp：当前时间戳，单位是毫秒，与请求调用时间误差不能超过1小时
    timestamp = int(round(time.time() * 1000))

    # 加密，获取sign和timestamp
    # data = (str(timestamp) + '\n' + secret).encode('utf-8')
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    data = string_to_sign.encode('utf-8')
    # secret = bytes(secret).encode('utf-8')
    signature = base64.b64encode(hmac.new(secret_enc, data, digestmod=hashlib.sha256).digest())
    # reg = re.compile(r"'(.*)'")
    # signature = str(re.findall(reg,str(signature))[0])
    signature = parse.quote(signature)

    # 发送信息
    # url = 'https://oapi.dingtalk.com/robot/send?access_token=%s&sign=%s&timestamp=%s' \
    if signature:
        url = '%s&sign=%s&timestamp=%s' % (access_token, signature, timestamp)
    else:
        url = '%s&timestamp=%s' % (access_token, timestamp)
    headers = {"Content-Type": "application/json ;charset=utf-8 "}
    try:
        response = requests.post(url, headers=headers, json=message, timeout=(3, 60))
        print(response)
        response_msg = str(response.status_code) + ' ' + str(response.content)
        print(response_msg)
    except Exception as error_msg:
        print('error_msg==='+str(error_msg))
        response_msg = error_msg

    return response_msg


if __name__ == "__main__":
    msg = {"msgtype": "text", "text": {"content": "测试"}, "at": {"isAtAll": False}}
    SendMessage(msg)
