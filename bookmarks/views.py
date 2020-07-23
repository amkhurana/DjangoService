#from django.shortcuts import render
#from rest_framework.views import APIView
from django.contrib.auth.models import Group
from django.http import HttpRequest
from django.views import View
from rest_framework import serializers,generics, permissions, status, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer


class IsPremiumUser(permissions.BasePermission):
    def has_object_permission(self, request: HttpRequest, view: View, obj):
        owns_object = (obj.user == request.user)
        return owns_object

    # def has_permission(self, request, view):
    #     return super().has_permission(request, view)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class BookmarkView(generics.ListCreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    # def get(self, request, format=None):
    #     bookmark = Bookmark.objects.all()
    #     serializer = BookmarkSerializer(bookmark, many=True)
    #     return Response(serializer.data)


class BookmarkViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsPremiumUser)
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def get_queryset(self): 
        return Bookmark.objects.filter(user=self.request.user)

    

    def create(self, request, *args, **kwargs):
        request_copy = request.POST.copy()
        request_copy['user'] = str(request.user.id)
        serializer = self.get_serializer(data=request_copy)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)