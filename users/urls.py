from django.urls import include, path
from .views import *
from rest_framework.routers import DefaultRouter, SimpleRouter

userrouter = SimpleRouter()
userrouter.register('', UserViewSet, basename="UserViewSet"),


urlpatterns = [
    ##############################AUTHENTICATION##############################
    
    path('auth/register', RegisterAPI.as_view(), name="register"),
    path('auth/login', LoginAPI.as_view(), name="login"),
    path('auth/logout', LogoutAPI.as_view(), name="logout"),
    ##########################################################################
    path('', include(userrouter.urls)),
]