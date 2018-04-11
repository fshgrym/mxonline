# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from .models import CourseOrg,CityDict,Teacher
from .forms import UserAskForm
from operations.models import UserFavorite
from courses.models import CourseOrg
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from courses.models import Courses

# Create your views here.
class OrgView(View):
    #课程机构的列表功能
    def get(self,request):
        all_orgs=CourseOrg.objects.all()
        hot_orgs=all_orgs.order_by('-click_nums')[:5]

        search_keywords = request.GET.get('keywords', '')#机构搜素
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        all_city=CityDict.objects.all()
        #取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs=all_orgs.filter(city_id=int(city_id))
        category=request.GET.get('ct','')
        if category:
            all_orgs=all_orgs.filter(category=category)
        #对课程机构进行分页
        sort=request.GET.get('sort','')
        if sort:
            if sort=='students':
                all_orgs=all_orgs.order_by('-students')
            elif sort=='course':
                all_orgs=all_orgs.order_by('-course_nums')

        orgs_nums = all_orgs.count()#不能过早把课程进行统计，需要筛选后进行统计
        try:
            page=request.GET.get('page',1)
        except PageNotAnInteger:
            page=1
        p=Paginator(all_orgs,3,request=request)#5等于几个数据分页

        orgs = p.page(page)
        return render(request,'org-list.html',
                      {'all_orgs':orgs,
                       'all_city':all_city,
                       'orgs_nums':orgs_nums,
                       'city_id':city_id,
                       'category':category,
                       'hot_orgs':hot_orgs,
                       'sort':sort,
                       })

class AddUserAskView(View):
    def post(self,request):
        userask_form=UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask=userask_form.save(commit=True)#直接自己提交保存到数据库
            return HttpResponse("{'status':'success'}",content_type="application/json")#浏览器自动解析成json
        else:
            return HttpResponse("{'status':'fail','msg':'提交失败'}",content_type="application/json")

class OrgHomeView(View):
    '''机构首页'''
    def get(self,request,org_id):
        current_page='home'
        course_org=CourseOrg.objects.get(id=int(org_id))

        has_fav=False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav=True

        all_course=course_org.courses_set.all()[:3]#取出所有外键
        all_teachers=course_org.teacher_set.all()[:2]#取出所有教师外键
        return render(request,'org-detail-homepage.html',{
            'all_course':all_course,
            'all_teachers':all_teachers,
            'course_org': course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })

class OrgCourseView(View):
    '''机构课程'''
    def get(self,request,org_id):
        current_page = 'course'
        course_org=CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_course=course_org.courses_set.all()#取出所有外键
        return render(request,'org-detail-course.html',{
            'all_course':all_course,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })

class OrgDescView(View):
    '''机构介绍'''
    def get(self,request,org_id):
        current_page = 'desc'
        course_org=CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-desc.html',{
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })

class OrgTeacherView(View):
    '''讲师页'''
    def get(self,request,org_id):
        current_page='teach'
        course_org=CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teachers=course_org.teacher_set.all()#取出所有教师外键
        return render(request,'org-detail-teachers.html',{
            'all_teachers':all_teachers,
            'course_org': course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })


class AddFacView(View):
    '''用户收藏，以及取消收藏'''
    def post(self,request):
        fav_id=request.POST.get('fav_id',0)
        fav_type=request.POST.get('fav_type',0)

        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type="application/json")
            #判断用户 登录状态
        exis_records=UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exis_records:
            '''如果已经有数据了，表示用户要取消收藏'''
            exis_records.delete()
            if int(fav_type) == 1:
                '''
                课程收藏
                '''
                course = Courses.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums =0
                course.save()
            elif int(fav_type) == 2:
                '''机构收藏'''
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -=1
                if course_org.fav_nums < 0:
                    course_org.fav_nums =0
                course_org.save()
            # elif int(fav_type) == 3:
            #     teacher = Teacher.objects.get(id=int(fav_id))
            #     teacher.fav_nums -=1
            #     teacher.save()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type="application/json")
        else:
            user_fav=UserFavorite()
            if int(fav_type) > 0 and int(fav_id) > 0:
                user_fav.user=request.user
                user_fav.fav_id=int(fav_id)
                user_fav.fav_type=int(fav_type)
                user_fav.save()
                if int(fav_type) == 1:
                    '''
                    课程收藏
                    '''
                    course = Courses.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    '''机构收藏'''
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1

                    course_org.save()
                # elif int(fav_type) == 3:
                #     teacher = Teacher.objects.get(id=int(fav_id))
                #     teacher.fav_nums -=1
                #     teacher.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"fail","msg":"收藏失败"}', content_type="application/json")


class TeacherLiseView(View):
    '''讲师列表页'''
    def get(self,request):
        all_teacher = Teacher.objects.all()

        search_keywords = request.GET.get('keywords', '')  # 机构搜素
        if search_keywords:
            all_teacher = all_teacher.filter(Q(name__icontains=search_keywords) | Q(work_position__icontains=search_keywords))

        sort = request.GET.get('sort','')
        if sort:
            if sort == 'host':
                all_teacher = all_teacher.order_by('-click_nums')

        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:5]#讲师排行
        try:#分页
            page=request.GET.get('page',1)
        except PageNotAnInteger:
            page=1
        p=Paginator(all_teacher,3,request=request)#5等于几个数据分页

        teachers = p.page(page)
        return render(request,'teachers-list.html',{'all_teacher':teachers,'sorted_teacher':sorted_teacher,'sort':sort})

class TeachDetailView(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        all_course = Courses.objects.filter(teacher=teacher)

        teacher.click_nums+=1
        teacher.save()

        #判断是否收藏
        has_teach_faved = False
        if UserFavorite.objects.filter(user=request.user,fav_type=3,fav_id=teacher.id):
            has_teach_faved = True
        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user,fav_type=2,fav_id=teacher.org.id):
            has_org_faved = True

        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:5]#讲师排行
        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'all_course':all_course,
            'sorted_teacher':sorted_teacher,
            'has_teach_faved':has_teach_faved,
            'has_org_faved':has_org_faved
        })