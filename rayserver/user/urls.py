from django.urls import path
from .views import UserRegist, UserLogin

app_name = "user"

urlpatterns = [    
    path('user_regist', UserRegist.as_view(), name='user_regist'),
    path('user_login', UserLogin.as_view(), name='user_login'),
]