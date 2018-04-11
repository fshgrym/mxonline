# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.utils.six import python_2_unicode_compatible
# Create your models here.


@python_2_unicode_compatible
class CityDict(models.Model):
    name=models.CharField(max_length=20,verbose_name=u'城市')
    desc=models.TextField(verbose_name=u'机构描述')
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name_plural=verbose_name=u'城市'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class CourseOrg(models.Model):
    name=models.CharField(max_length=50,verbose_name=u'机构名称')
    desc=models.TextField(verbose_name=u'机构描述')
    tag = models.CharField(max_length=10,default='全国知名',verbose_name='机构标签')
    category=models.CharField(choices=(('pxjg','培训机构'),('gx','高校'),('gr','个人')),max_length=20,verbose_name='培训类别',default='pxjg')
    click_nums=models.IntegerField(default=0,verbose_name=u'点击数')
    fav_nums=models.IntegerField(default=0,verbose_name=u'收藏数')
    image=models.ImageField(upload_to='org/%Y/%m',verbose_name=u'封面图',max_length=100)
    address=models.CharField(max_length=150,verbose_name=u'机构地址')
    students=models.IntegerField(default=0,verbose_name=u'学习人数')
    course_nums=models.IntegerField(default=0,verbose_name=u'课程数')
    city=models.ForeignKey(CityDict,verbose_name=u'所在城市')

    class Meta:
        verbose_name_plural=verbose_name=u'机构'

    def __str__(self):
        return self.name

    def get_teach_nums(self):#获取课程机构的教师人数
        return self.teacher_set.all().count()


@python_2_unicode_compatible
class Teacher(models.Model):
    org=models.ForeignKey(CourseOrg,verbose_name=u'所属机构')
    name=models.CharField(max_length=50,verbose_name=u'教师名字')
    work_years=models.IntegerField(default=0,verbose_name=u'工作年限')
    work_company=models.CharField(max_length=50,verbose_name=u'就职公司')
    work_position=models.CharField(max_length=50,verbose_name=u'公司职位')
    image = models.ImageField(upload_to='teach/%Y/%m', verbose_name=u'头像', max_length=100,null=True)
    points= models.CharField(max_length=50,verbose_name=u'教学特点')
    click_nums = models.IntegerField(default=0,verbose_name='点击数')
    age = models.IntegerField(default=18,verbose_name='年龄')
    add_time=models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name_plural=verbose_name=u'教师'

    def __str__(self):
        return self.name

    def get_course_num(self):
        return self.courses_set.all().count()