"""DjangoService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth.models import Group, Permission
from django.urls import path, include
#rom rest_framework.routers import DefaultRouter
from rest_framework import serializers, viewsets, routers
from bookmarks.serializers import UserSerializer, GroupSerializer, GroupPermissionSerializer
#from bookmarks.models import Bookmark
from localusers.models import LocalUser
from bookmarks.views import BookmarkViewSet
import localusers.views


class UserViewSet(viewsets.ModelViewSet):
    queryset = LocalUser.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupPermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = GroupPermissionSerializer


router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('groups', GroupViewSet)
router.register('bookmarks', BookmarkViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/auth/', include('rest_framework.urls')),
     path('api/login/', localusers.views.api_login),
    path('api/logout/', localusers.views.api_logout),
    path('api/', include(router.urls)),
    #path('', include('api_basic.urls')),
   
]