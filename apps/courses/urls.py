#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
#time:'2017/12/9 13:44:56下午'
from django.conf.urls import url,include
from .views import CourseListView,CourseDetailView,CourseVideoView,CommentsView,AddCommentView

urlpatterns = [
    # '''课程列表页'''
    url(r'^list/$',CourseListView.as_view(),name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$',CourseDetailView.as_view(),name='course_detail'),
    url(r'^info/(?P<course_id>\d+)/$',CourseVideoView.as_view(),name='course_video'),
    url(r'^comment/(?P<course_id>\d+)/$',CommentsView.as_view(),name='course_comment'),#课程评论
    url(r'^add_comment/$',AddCommentView.as_view(),name='add_comment'),#课程评论
]