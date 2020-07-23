from django.contrib.auth.models import  Group, Permission
from rest_framework import serializers
from bookmarks.models import Bookmark
#from rest_framework import serializers, viewsets, routers, generics, permissions, mixins
#from rest_framework.viewsets import GenericViewSet
from localusers.models import LocalUser




class UserSerializer(serializers.HyperlinkedModelSerializer):
    bookmarks = serializers.PrimaryKeyRelatedField(many=True, queryset=Bookmark.objects.all())
    class Meta:
        model = LocalUser
        fields = ('url', 'username', 'email', 'is_staff', 'bookmarks')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('latitude', 'longitude', 'user')


class GroupPermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'url', 'name', 'codename')