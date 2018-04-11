#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
#time:'2017/11/28 22:40:31下午'
from random import Random

from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from MxOnline.settings import DEFAULT_FROM_EMAIL


def send_register_email(email,send_type='regidter'):
    email_record = EmailVerifyRecord()
    if send_type =='upemail':
        code =random_str(4)
    else:
        code = random_str(16)
    email_record.code=code
    email_record.email=email
    email_record.send_type=send_type
    email_record.save()

    email_title=''
    email_body=''
    if send_type == 'register':
        email_title='幕学在线网注册激活链接'
        email_body='请点击下面的来激活你的账号：http://127.0.0.1:8000/active/{}'.format(code)
        send_mail(email_title,email_body,DEFAULT_FROM_EMAIL,[email])
        # if send_status:
        #     return 'aaa'
        # else:
        #     return 'aaa'
    elif send_type=='forget':
        email_title = '幕学在线网密码重置链接'
        email_body = '请点击下面的来重置你的密码：http://127.0.0.1:8000/reset/{}'.format(code)
        send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [email])
    elif send_type == 'upemail':
        email_title = '幕学在线网邮箱修改链接'
        email_body = '你的邮箱验证码是：{0}'.format(code)
        send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [email])

def random_str(randomlength=8):
    str = ''
    chars = 'ADgggGGSGDGDHSGgdbdagagdgG561254754153615'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str

# def generate_random_str():
#     pass
