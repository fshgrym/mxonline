# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.utils.six import python_2_unicode_compatible
from DjangoUeditor.models import UEditorField
from organization.models import CourseOrg,Teacher
# Create your models here.
@python_2_unicode_compatible
class Courses(models.Model):
    course_org=models.ForeignKey(CourseOrg,verbose_name=u'课程机构',null=True,blank=True)
    name=models.CharField(max_length=50,verbose_name=u'课程名')
    desc=models.CharField(max_length=300,verbose_name=u'课程描述')
    teacher=models.ForeignKey(Teacher,verbose_name='讲师',null=True,blank=True)
    detail=UEditorField(verbose_name='课程详情',width=600, height=300, imagePath="course/ueditor/", filePath="course/ueditor/", default='')
    is_banner = models.BooleanField(default=False,verbose_name='是否轮播')
    degree=models.CharField(choices=(('cj',u'初级'),('zj',u'中级'),('gj','高级')),max_length=2,verbose_name='难度')
    learn_times=models.IntegerField(default=0,verbose_name=u'学习时长(分钟)')
    students=models.IntegerField(default=0,verbose_name=u'学习人数')
    fav_nums=models.IntegerField(default=0,verbose_name=u'收藏人数')
    image=models.ImageField(upload_to='courses/%Y/%m',verbose_name=u'封面图',max_length=100)
    click_nums=models.IntegerField(default=0,verbose_name=u'点击数')
    youneed_know = models.CharField(max_length=300,verbose_name='课程须知',default='')
    teacher_tell = models.CharField(max_length=300,verbose_name='老师告诉你能学到什么',default='')
    tag=models.CharField(default='',verbose_name='课程标签',max_length=10)
    category = models.CharField(max_length=20, verbose_name=u'课程类别',default='后端开发')
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name_plural=verbose_name=u'课程'

    def __str__(self):
        return self.name

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<a href="http://www.projectsedu.com">跳转</a>')

    go_to.short_description='跳转'
    def get_zj_nums(self):
        '''获取课程章节数'''
        return self.lesson_set.all().count()

    get_zj_nums.short_description = '章节'

    def get_learn_users(self):#获取学习该课程的用户
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):#获取课程所有章节
        return self.lesson_set.all()
class BannerCourse(Courses):
    class Meta:
        verbose_name_plural=verbose_name='轮播课程'
        proxy = True #不生成表
@python_2_unicode_compatible
class Lesson(models.Model):
    course=models.ForeignKey(Courses,verbose_name=u'课程')
    name = models.CharField(max_length=100,verbose_name=u'章节名')
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name_plural=verbose_name=u'章节'

    def __str__(self):
        return self.name

    def get_lesson_video(self):#获取章节里面所有的视频
        return self.video_set.all()

@python_2_unicode_compatible
class Video(models.Model):
    lesson=models.ForeignKey(Lesson,verbose_name=u'章节')
    name=models.CharField(max_length=100,verbose_name=u'视频名')
    url = models.CharField(max_length=200,verbose_name='访问地址',default='')
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟)')

    class Meta:
        verbose_name_plural=verbose_name=u'视频'

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class CoursesResource(models.Model):
    course=models.ForeignKey(Courses,verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    download=models.FileField(upload_to='course/resource/%Y/%m',verbose_name=u'资源文件',max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name_plural=verbose_name=u'课程资源'

    def __str__(self):
        return self.name