#views.py
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .serializer import LoginUserSerializer
from .models import LoginUser
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
# Create your views here.

class UserLogin(APIView):
    def post(self, request):
        user_id = request.data.get('user_id', "")
        user_pw = request.data.get('user_pw', "")
        user = LoginUser.objects.filter(user_id=user_id).first()
        if user is None:
            return Response(dict(msg="해당 ID의 사용자가 없습니다."))
        if check_password(user_pw, user.user_pw):
            return Response(dict(msg="로그인 성공", user_id=user.user_id, birth_day=user.birth_day,
                                 gender=user.gender, email=user.email, name=user.name, age=user.age))
        else:
            return Response(dict(msg="로그인 실패. 패스워드 불일치"))
        
class UserRegist(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(request.data)

        if LoginUser.objects.filter(user_id=serializer.data['user_id']).exists():
            # DB에 있는 값 출력할 때 어떻게 나오는지 보려고 user 객체에 담음
            user = LoginUser.objects.filter(user_id=serializer.data['user_id']).first()
            data = dict(
                msg="이미 존재하는 아이디입니다.",
                user_id=user.user_id,
                user_pw=user.user_pw,
                code="400"
            )
            return Response(data)
        user = serializer.create(request.data)
        return Response(data=dict(LoginUserSerializer(user).data, code="200",msg="성공"))



