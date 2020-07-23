from django.contrib import admin
from django.contrib.auth.models import User, Group
from bookmarks.models import Bookmark

# Register your models here.
#admin.site.register(User)
#admin.site.register(Group)
admin.site.register(Bookmark)