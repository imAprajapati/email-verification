from unicodedata import name
from django.urls import path
from .views import *

urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('signup/',Signup.as_view(),name='signup'),
    path('user-verification/<slug:token>',user_verifiaction,name='user-verification'),
    path('login/',Login.as_view(),name='login'),
    path('logout/',user_logout,name='logout'),
    path('forget-password/',ForgetPassword.as_view(),name='forget-password'),
    path('forget-verification/<str:username>/<slug:token>',ChangePassword.as_view(),name='forget-verification'),
    path('forget-verification/change-password/',change_password,name='change-password')
]
