#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
#time:'2017/11/26 22:28:47下午'
import xadmin

from .models import CourseOrg,CityDict,Teacher


class CourseOrgAdmin(object):
    list_display=['name','desc','click_nums','fav_nums','image','address','city']
    search_fields=['name','desc','address','city']
    list_filter=['name','desc','click_nums','fav_nums','image','address','city']
    relfield_style = 'fk-ajax'  # 当某个models以他做为外键，加载会是ajax模式


class CityDictAdmin(object):
    list_display=['name','desc','add_time']
    search_fields=['name','desc']
    list_filter=['name','desc','add_time']


class TeacherAdmin(object):
    list_display=['org','name','work_years','work_company','work_position','points','add_time']
    search_fields=['org','name','work_years','work_company','work_position','points']
    list_filter=['org','name','work_years','work_company','work_position','points','add_time']


xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(Teacher,TeacherAdmin)