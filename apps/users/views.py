# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.contrib.auth import authenticate,logout,login#验证用户名密码,
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View#可以通过views来做登录
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse

import json

from pure_pagination import Paginator,PageNotAnInteger,EmptyPage
from courses.models import Courses
from organization.models import CourseOrg,Teacher
from operations.models import UserCourse,UserFavorite,UserMessage
from .models import UserProfile,EmailVerifyRecord,Banner
from .forms import UploadImageForm,UserInfoForm
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm
from utils.email_send import send_register_email
from utils.minxin_utils import LoginRequiredMixin
# 登录（需要设置seeting AUTHENTICATION_BACKENDS=(
#     'users.views.CustomBackend',
# )）


class CustomBackend(ModelBackend):#会调用我门写的login的views函数
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user=UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class LogoutView(View):
    def get(self,request):
        logout(request)
        '''
        重定向
        '''
        from django.core.urlresolvers import reverse#反解name
        return HttpResponseRedirect(reverse('index'))


# 通过继承Views完成登录，会自动调用get和post方法,推荐使用
class LoginView(View):
    def get(self,request):
        return render(request, 'login.html')

    def post(self,request):
        login_form=LoginForm(request.POST)#验证
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)#自动验证
            if user is not None:
                if user.is_active:

                    login(request, user)  # 完成验证后登录
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request,'login.html',{'msg':'用户未激活'})
            else:
                msg = '用户名或者密码错误！'
                return render(request, 'login.html', {'msg': msg})
        else:
            msg = '用户名或者密码错误！'
            return render(request, 'login.html', {'msg': msg,'login_form':login_form})



#函数式登录逻辑，建议使用类来做（作废）
def user_login(request):
    if request.method=='POST':
        user_name=request.POST.get('username','')
        pass_word=request.POST.get('password','')
        user=authenticate(username=user_name,password=pass_word)
        if user is not None:
            login(request,user)#完成验证后登录
            return render(request,'index.html',)
        else:
            msg='用户名或者密码错误！'
            return render(request,'login.html',{'msg':msg})
    return render(request,'login.html')


class RegisterView(View):
    def get(self,request):
        register_form=RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self,request):
        register_form=RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request,'register.html',{'msg':'用户已经存在！！','register_form':register_form})
            pass_word = request.POST.get('password', '')
            user_profile=UserProfile()
            user_profile.username=user_name
            user_profile.email=user_name
            user_profile.password=make_password(pass_word)#加密
            user_profile.is_active = False
            user_profile.save()
            send_register_email(user_name, 'register')

            #写入消息
            user_message = UserMessage()
            user_message.user = user_profile
            user_message.message = '欢迎注册慕课网'
            user_message.save()

            return render(request,'login.html')
        else:
            return render(request,'register.html',{'register_form':register_form})

class ActiveViews(View):
    def get(self,request,active_code):
        all_recodes=EmailVerifyRecord.objects.filter(code=active_code)
        if all_recodes:
            for recode in all_recodes:
                email=recode.email
                user=UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request,'active_fail.html')
        return render(request,'login.html')


class ResetViews(View):
    def get(self,request,active_code):
        all_recodes=EmailVerifyRecord.objects.filter(code=active_code)
        if all_recodes:
            for recode in all_recodes:
                email=recode.email
                return render(request,'password_reset.html',{'email':email})
        else:
            return render(request,'active_fail.html')
        return render(request,'login.html')
class ModifyPwd(View):
    '''
    修改用户密码
    '''
    def post(self,request):
        modify_form=ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get('password','')
            pwd2=request.POST.get('password2','')
            email=request.POST.get('email','')
            if pwd1!=pwd2:
                return render(request,'password_reset.html',{'email':email,'msg':'密码不一致！','modify_form':modify_form})
            user=UserProfile.objects.get(email=email)
            user.password=make_password(pwd2)
            user.save()
            return render(request,'login.html')
        else:
            email=request.POST.get('email','')
            return render(request,'password_reset.html',{'email':email,'modify_form':modify_form})


class ForgetPwdView(View):
    def get(self,request):
        forget_form=ForgetForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})
    def post(self,request):
        forget_form=ForgetForm(request.POST)
        if forget_form.is_valid():
            email=request.POST.get('email','')
            send_register_email(email,'forget')
            return render(request,'send_success.html')
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})


class UserinfoView(LoginRequiredMixin,View):
    '''
    用户个人信息
    '''
    def get(self,request):
        return render(request,'usercenter-info.html')
    def post(self,request):
        '''
        用户信息提交
        :param request:
        :return:
        '''
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')

class UploadImageViwe(LoginRequiredMixin,View):
    '''
    用户修改头像
    '''
    def post(self,request):
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            request.user.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

class ModifyPwdView(View):
    '''
    修改个人中心用户密码
    '''
    def post(self,request):
        modify_form=ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get('password','')
            pwd2=request.POST.get('password2','')
            if pwd1!=pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user=request.user
            user.password=make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')

class SendEmailCodeView(LoginRequiredMixin,View):
    '''
    必须登录后才能操作
    发送邮箱验证码
    '''
    def get(self,request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}',content_type='application/json')
        send_register_email(email,'upemail')
        return HttpResponse('{"status":"success"}', content_type='application/json')
class UpdateEmailView(LoginRequiredMixin,View):
    '''
    修改个人邮箱验证接口
    '''
    def post(self,request):
        email = request.POST.get('email','')
        code = request.POST.get('code','')
        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type='upemail')
        if existed_records:
            user =request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码错误"}', content_type='application/json')

class MyCourseView(LoginRequiredMixin,View):
    '''
    我的课程
    '''
    def get(self,request):
        user_course = UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{'user_courses':user_course})

class MyFavOrgView(LoginRequiredMixin,View):
    '''
    收藏课程
    '''
    def get(self,request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request,'usercenter-fav-org.html',{'org_list':org_list})
class MyFavTeacherView(LoginRequiredMixin,View):
    '''
    收藏教师
    '''
    def get(self,request):
        teach_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teach_id = fav_teacher.fav_id
            teach = Teacher.objects.get(id=teach_id)
            teach_list.append(teach)
        return render(request,'usercenter-fav-teacher.html',{'teach_list':teach_list})
class MyFavCourseView(LoginRequiredMixin,View):
    '''
    收藏课程
    '''
    def get(self,request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Courses.objects.get(id=course_id)
            course_list.append(course)

        return render(request,'usercenter-fav-course.html',{'course_list':course_list})
class MymessageView(LoginRequiredMixin,View):
    '''
    我的 消息
    '''
    def get(self,request):
        all_message = UserMessage.objects.filter(user=request.user.id,has_read=False)
        for unread_message in all_message:
            unread_message.has_read = True
            unread_message.save()
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page =1
        p = Paginator(all_message,5,request=request)
        messages = p.page(page)
        return render(request,'usercenter-message.html',{'messages':messages})

class IndexView(View):
    '''
    幕学在线网首页
    '''
    def get(self,request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Courses.objects.filter(is_banner=False)[:6]
        banners_courses = Courses.objects.filter(is_banner=True)[:3]
        course_orgs =CourseOrg.objects.all()[:15]
        return render(request,'index.html',
                      {'all_banners':all_banners,
                       'courses':courses,
                       'banners_courses':banners_courses,
                       'course_orgs':course_orgs,
                       })
def page_not_fount(request):
    response = render_to_response('404.html')
    response.status_code = 404
    return  response

def page_error(request):
    response = render_to_response('500.html')
    response.status_code = 500
    return  response