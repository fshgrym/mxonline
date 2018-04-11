# -*- coding:utf-8 -*-
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.views.static import serve#用于处理静态文件
from django.conf.urls import url,include
from django.views.generic import TemplateView
# from django.contrib import admin
import xadmin

from MxOnline.settings import MEDIA_ROOT
from users.views import user_login,LoginView,LogoutView,RegisterView,ActiveViews,ForgetPwdView,ResetViews,ModifyPwd,IndexView
from organization.views import OrgView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$',IndexView.as_view(),name='index'),#TemplateView.as_view(template_name='index.html')
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    url(r'^register/$',RegisterView.as_view(),name='register'),
    url(r'^captcha/',include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$',ActiveViews.as_view(),name='active_code'),
    url(r'^reset/(?P<active_code>.*)/$',ResetViews.as_view(),name='reset_pwt'),
    url(r'^modify/$',ModifyPwd.as_view(),name='modify_pwd'),
    url(r'^forget/$',ForgetPwdView.as_view(),name='forgetpwd'),

    url(r'^org/',include('organization.urls',namespace='org')),#namespace增加命名空间，includeu rl分发 机构和讲师
    url(r'^course/',include('courses.urls',namespace='course')),#namespace增加命名空间，includeu rl分发 课程相关
    # url(r'^teacher/',include('courses.urls',namespace='course')),#namespace增加命名空间，includeu rl分发 讲师
    url(r'users/',include('users.urls',namespace='users')),
    url(r'^media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT}),#配置文件上传访问的url
    # url(r'^static/(?P<path>.*)$',serve,{'document_root':STATIC_ROOT}),#配置文件上传访问的url
    url(r'^ueditor',include('DjangoUeditor.urls'))
]

#全局404 500
handler404 = 'users.views.page_not_fount'
handler500 = 'users.views.page_error'
# handler503 = 'users.view.page_error'
