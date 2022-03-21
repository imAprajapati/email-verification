import http
from lib2to3.pgen2 import token
from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.

class Home(View):
    def get(self,request):
        return render(request,'home.html')

    
def token_verify(token,email):
    subject='verify your email'
    message=f'hi click on the here http://127.0.0.1:8000/user-verification/{token}'
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email]
    print(email)
    send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list)

class Signup(View):
    def get(self,request):
        return render(request,'signup.html')
    def post(self,request):
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        object_user=User.objects.create_user(username,email,password)
        uid=uuid.uuid4()
        profile_object=Profile(user=object_user,token=uid)
        profile_object.save()

        # token verification function call

        token_verify(uid,object_user.email)   

        messages.success(request,'Veryfication link send on your email !!')
        return redirect('/signup/')

def user_verifiaction(request,token):
    profile_object=Profile.objects.get(token=token)
    if profile_object is not None:
        profile_object.verify=True
        profile_object.save()
        messages.success(request,'your email have verified')
        return redirect('/login/')
    else:
        return HttpResponse('<h4> unknown user <h4>')
    # return HttpResponse('<h4>login successfully !!</h4>')


class Login(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']
        user_obj=User.objects.get(username=username)
        user=authenticate(request,username=username,password=password)
        # print(user)
        if user is not None:
            profile_obj = Profile.objects.get(user=user_obj)
            if profile_obj.verify:
                login(request,user_obj)
                return redirect('/')
            else:
                messages.info(request,'Please check your email and verify your account')
                return redirect('/login/')
        else:
            messages.info(request,'Signup your account')
            return redirect('/signup/')


def user_logout(request):
    logout(request)
    return redirect('/')

def forget_verification(username,email,token):
    subject='forget password'
    messages=f'hi click on the here http://127.0.0.1:8000/forget-verification/{username}/{token}'
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject=subject,message=messages,from_email=from_email,recipient_list=recipient_list)


class ForgetPassword(View):
    def get(self,request):
        return render(request,'forget_password.html')
    def post(self,request):
        username=request.POST['username']
        try:
            user=User.objects.get(username=username)
            uid=uuid.uuid4()
            forget_verification(username,user.email,uid)  
            messages.success(request,'check your email to forget password')
            return redirect('/forget-password/')          
        except:
            messages.warning(request,'username not exit')
            return redirect('/forget-password/')
        # return redirect('/forget-password/')


class ChangePassword(View):
    def get(self,request,username,token):
        return render(request,'change-password.html',{'username':username})



def change_password(request):
    if request.method=='POST':
        password=request.POST['password']
        cpassword=request.POST['con-password']
        username=request.POST['username']
        user=User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(password,cpassword,username)
        return HttpResponse('password change successfully !!')