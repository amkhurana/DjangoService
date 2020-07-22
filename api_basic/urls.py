
from django.urls import path, include
from .views import article_list, articledetail, ArticleView, ArticleDetail, GenericView, ArticleViewSet, ArticleGenericViewSet, ArticleModelViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
#router.register('article', ArticleViewSet, basename='art')
#router.register('article', ArticleGenericViewSet, basename='art')
router.register('article', ArticleModelViewSet, basename='art')

urlpatterns = [
    #path('article/', article_list),
    #path('detail/<int:pk>/', ArticleDetail.as_view())
    path('viewset/', include(router.urls)),
     path('viewset/<int:pk>/', include(router.urls)),
    path('article/', ArticleView.as_view()),
    path('detail/<int:id>/', ArticleDetail.as_view()),
    path('genericarticle/<int:id>/', GenericView.as_view())

]