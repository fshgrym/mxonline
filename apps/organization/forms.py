#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
#time:'2017/12/2 16:44:52下午'
import re

from operations.models import UserAsk

from django import forms

class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']

    def clean_mobile(self):
        '''验证手机号码是否正确，验证函数必须以clean_xxx开头，form会自己调用'''
        mobile=self.cleaned_data['mobile']
        REGEX_MOBILE="^1[358]\d{9}$|^176\d{8}$"
        p=re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:#自己抛出异常
            raise  forms.ValidationError('手机号码非法',code='mobile_invalid')