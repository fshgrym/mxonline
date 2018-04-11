#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
#time:'2017/11/26 21:11:44下午'
from organization.models import  CourseOrg
from .models import Courses,CoursesResource,Lesson,Video,BannerCourse
import xadmin

class LessonInline(object):
    model = Lesson
    extra = 0
class CourseResourceInline(object):
    model = CoursesResource
    extra = 0
class BannerCourseAdmin(object):
    ordering = ['-click_nums'] #排序
    # readonly_fields = ['click_nums']#设置只读，无法编辑
    exclude = ['fav_nums']#设置这个进入编辑后看不到
    list_display=['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']
    search_fields=['name','desc','detail','degree','students']
    list_filter=['name','desc','detail','degree','learn_times','students','fav_nums','click_nums','add_time']
    inlines = [LessonInline,CourseResourceInline]
    def queryset(self):
        #只会显示queryset后的数据
        qs = super(BannerCourseAdmin, self).queryset()#重载父类
        qs = qs.filter(is_banner=True)
        return qs
class CoursesAdmin(object):
    ordering = ['-click_nums'] #排序
    # readonly_fields = ['click_nums']#设置只读，无法编辑
    exclude = ['fav_nums']#设置这个进入编辑后看不到
    list_display=['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time','get_zj_nums','go_to']
    search_fields=['name','desc','detail','degree','students']
    list_filter=['name','desc','detail','degree','learn_times','students','fav_nums','click_nums','add_time']
    list_editable = ['degree','desc']
    inlines = [LessonInline,CourseResourceInline]
    refresh_times = [3,5]#定时刷新
    style_fields = {'detail':'ueditor'}
    import_excel = True
    def queryset(self):
        #只会显示queryset后的数据
        qs = super(CoursesAdmin, self).queryset()#重载父类
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Courses.objects.filter(course_org=course_org).count()
            course_org.save()
    def post(self,request,*args,**kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CoursesAdmin, self).post(request,args,kwargs)

class CoursesResourceAdmin(object):
    list_display=['course','name','download','add_time']
    search_fields=['course','name','download']
    list_filer=['course__name','name','download','add_time']


class LessonAdmin(object):
    list_display=['course','name','add_time']
    search_fields=['course','name']
    list_filter=['course','name','add_time']


class VideoAdmin(object):
    list_display=['lesson','name','add_time']
    search_fields=['lesson','name']
    list_filter=['lesson','name','add_time']


xadmin.site.register(Courses,CoursesAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)
xadmin.site.register(CoursesResource,CoursesResourceAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
