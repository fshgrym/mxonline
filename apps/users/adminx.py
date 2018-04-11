#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
#time:'2017/11/26 20:06:22下午'
import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin


from .models import EmailVerifyRecord,Banner,UserProfile

class UserProfileAdmin(UserAdmin):
    pass
class BaseSetting(object):
    enable_themes=True #xadmin默认关闭主题功能
    use_bootswatch=True


class GlobalSettings(object):
    site_title='幕学后台管理系统'
    site_footer='幕学在线网'
    menu_style='accordion'


class EmailVerifyRecordAdmin(object):
    model_icon = 'fa fa-address-book-o'
    list_display=['code','email','send_type','send_time']
    search_fields=['code','email','send_type']
    list_filter=['code','email','send_type','send_time']


class BannerAdmin(object):
    list_display=['title','image','url','index','add_time']
    search_fields=['title','image','url','index']
    list_filter=['title','image','url','index','add_time']

# xadmin.site.unregister()卸载默认注册app
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
# xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)