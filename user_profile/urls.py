
# 登录注册
from django.urls import path, include
from rest_framework.authtoken import views
from . import views as view2
from rest_framework_jwt.views import obtain_jwt_token



app_name = 'user_profile'

urlpatterns = [
    path('login/', view2.LoginView.as_view(), name='login'),
    path('register/', view2.RegisterView.as_view(), name='register'),
]


urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token),
    path('jwt-auth/', obtain_jwt_token)
]