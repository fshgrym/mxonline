#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
# time:'2017/12/2 17:14:49下午'
from django.conf.urls import url,include
from .views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,AddFacView,TeacherLiseView,TeachDetailView
urlpatterns = [
    url(r'^list/$',OrgView.as_view(),name='org_list'),#课程机构首页’，
    url(r'^add_ask/$',AddUserAskView.as_view(),name='add_ask'),#课程机构首页’，
    url(r'^home/(?P<org_id>\d+)/$',OrgHomeView.as_view(),name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$',OrgCourseView.as_view(),name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$',OrgDescView.as_view(),name='org_desc'),
    url(r'^teach/(?P<org_id>\d+)/$',OrgTeacherView.as_view(),name='org_teach'),

    url(r'^add_fav/$',AddFacView.as_view(),name='add_fav'),#机构收藏

    #讲师列表页
    url(r'^teacher/list/$',TeacherLiseView.as_view(),name='teacher_list'),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$',TeachDetailView.as_view(),name='teacher_detail')
]