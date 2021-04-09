"""gaoxiaoyq URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

#加载静态界面index首页
def index(request):
    request.META["CSRF_COOKIE_USED"] = True
    return render(request, '')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/news/', include("hot_news.urls", namespace='hot_news')),
    path('api/user/', include("user_profile.urls", namespace='profile')),
    path('', index, name="index")
]
