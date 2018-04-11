# -*- coding:utf-8 -*-
from django.shortcuts import render
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.
from utils.minxin_utils import LoginRequiredMixin
from.models import Courses,CoursesResource
from operations.models import UserFavorite,CourseComments,UserCourse




class CourseListView(LoginRequiredMixin,View):
    def get(self,request):
        all_course=Courses.objects.all().order_by('-add_time')
        hot_courses = Courses.objects.all().order_by('-click_nums')[:3]
        #搜素功能
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_course = all_course.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))#icontains 会使用sql语句操作 django的i一般意思不区分大小写

        # 课程排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_course = all_course.order_by('-students')
            elif sort == 'hot':
                all_course = all_course.order_by('-click_nums')
        try:
            page=request.GET.get('page',1)
        except PageNotAnInteger:
            page=1
        p=Paginator(all_course,3,request=request)#5等于几个数据分页
        course = p.page(page)
        return render(request,'course-list.html',{
            'all_course':course,
            'sort':sort,
            'hot_courses':hot_courses,
        })


class CourseDetailView(View):
    '''课程详情页'''

    def get(self,request,course_id):
        course=Courses.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 前端功能暂时没有实现
        has_fav_course=False
        has_fav_org=False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type=1):
                has_fav_course=True
            if UserFavorite.objects.filter(user=request.user,fav_id=course.course_org.id,fav_type=2):
                has_fav_org=True

        tag=course.tag
        if tag:
            relate_courses=Courses.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request,'course-detail.html',{
            'course':course,
            'relate_course':relate_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org,
        })


class CourseVideoView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        '''课程章节视频信息'''
        course=Courses.objects.get(id=int(course_id))
        course.students +=1
        course.save()
        # 查询用户是否关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course=UserCourse(user=request.user,course=course)
            user_course.save()

        # 用户还学过什么课程
        user_cours = UserCourse.objects.filter(course=course)
        user_ids = [user_cour.user.id for user_cour in user_cours]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_coure.course.id for user_coure in all_user_courses]
        relate_courses = Courses.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_resources=CoursesResource.objects.filter(course=course)
        return render(request,'course-video.html',
        {
            'course':course,
            'all_resources':all_resources,
            'relate_courses':relate_courses,
        })


class CommentsView(View):
    def get(self,request,course_id):
        course = Courses.objects.get(id=int(course_id))
        all_resources = CoursesResource.objects.filter(course=course)
        all_comment = CourseComments.objects.all()
        return render(request,'course-comment.html',{
            'course':course,
            'all_resources':all_resources,
            'all_comment':all_comment,
        })


class AddCommentView(View):
    '''用户添加评论信息'''
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type="application/json")
            #判断用户 登录状态
        course_id = request.POST.get('course_id',0)
        comment = request.POST.get('comments',0)
        if course_id > 0 and comment:
            course_comment = CourseComments()
            course = Courses.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.comments = comment
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status":"success","msg":"评论成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","msg":"评论失败"}', content_type="application/json")
