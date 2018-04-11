#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
#time:'2017/11/26 21:32:49下午'
from .models import UserAsk,UserFavorite,CourseComments,UserCourse,UserMessage

import xadmin


class UserMessageAdmin(object):
    list_display=['user','message','has_read','add_time']
    search_fields=['user','message','has_read']
    list_filter=['user','message','has_read','add_time']


class UserAskAdmin(object):
    list_display=['name','mobile','course_name','add_time']
    search_fields=['name','mobile','course_name']
    list_filter=['name','mobile','course_name','add_time']


class UserFavoriteAdmin(object):
    list_display=['user','fav_id','fav_type','add_time']
    search_fields=['user','fav_id','fav_type']
    list_filter=['user','fav_id','fav_type','add_time']


class CourseCommentsAdmin(object):
    list_display=['user','course','comments','add_time']
    search_fields=['user','course','comments']
    list_filter=['user','course','comments','add_time']


class UserCourseAdmin(object):
    list_display=['user','course','add_time']
    search_fields=['user','course']
    list_filter=['user','course','add_time']


xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)