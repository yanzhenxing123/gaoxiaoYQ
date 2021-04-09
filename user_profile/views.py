from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import UserLoginSerializer, UserRegisterSerializer
from django.contrib.auth import authenticate, login, logout

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class LoginView(APIView):
    def post(self, request):
        res = {}
        data = request.data
        serializer = UserLoginSerializer(data=data)
        is_valid = serializer.is_valid()
        if not is_valid:
            res['code'] = 40001
            res['error'] = serializer.errors
            return Response(res)

        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            print(request.user)
            res['code'] = 200
            res['msg'] = '登录成功'
            res['data'] = {
                'user_id': user.id,
                'user_name': username,
            }
            return JsonResponse(res)
        else:
            res['code'] = 10002
            res['msg'] = '用户名或密码错误'
            return JsonResponse(res)


class RegisterView(APIView):
    def post(self, request):
        res = {}
        data = request.data
        serializer = UserRegisterSerializer(data=data)
        is_valid = serializer.is_valid()
        if not is_valid:
            res['code'] = 40003
            res['error'] = serializer.errors
            return JsonResponse(res)
        data = serializer.data
        try:
            uid = serializer.create(data)
        except Exception as e:
            res['code'] = 40004
            res['error'] = e
            return JsonResponse(res)

        res['code'] = 200
        res['data'] = {
            'uid': uid,
            'username': data['username'],
        }
        return JsonResponse(res)




