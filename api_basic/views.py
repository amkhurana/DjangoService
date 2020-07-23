from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleModelSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, mixins, generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly
from django.shortcuts import get_object_or_404


class ArticleModelViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleModelSerializer
    queryset = Article.objects.all()



class ArticleGenericViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    serializer_class = ArticleModelSerializer
    queryset = Article.objects.all()


class ArticleViewSet(viewsets.ViewSet):
    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleModelSerializer(articles, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArticleModelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = ArticleModelSerializer(article)
        return Response(serializer.data)

    def update(self, request, pk=None):
        article = Article.objects.get(pk=pk)
        serializer = ArticleModelSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenericView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = ArticleModelSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'
    #authentication_classes = (SessionAuthentication, BasicAuthentication)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)
    
    def delete(self, request, id=None):
        return self.destroy(request, id)



class ArticleView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleModelSerializer(articles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ArticleModelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetail(APIView):
    def get_object(self, id):
        try:
            return Article.objects.get(id=id)
    
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        article = self.get_object(id)
        serializer = ArticleModelSerializer(article)
        return Response(serializer.data)
    
    def put(self, request, id):
        article = self.get_object(id)
        serializer = ArticleModelSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @csrf_exempt
# def article_list(request):
#     if (request.method == 'GET'):
#         articles = Article.objects.all()
#         serializer = ArticleModelSerializer(articles, many=True)
#         return JsonResponse(serializer.data, safe = False)
    
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = ArticleModelSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# @csrf_exempt
# def articledetail(request,pk):
#     try:
#         article = Article.objects.get(pk=pk)
    
#     except Article.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = ArticleModelSerializer(article)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = ArticleModelSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         article.delete()
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def article_list(request):
    if (request.method == 'GET'):
        articles = Article.objects.all()
        serializer = ArticleModelSerializer(articles, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ArticleModelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET', 'PUT', 'DELETE'])
def articledetail(request,pk):
    try:
        article = Article.objects.get(pk=pk)
    
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ArticleModelSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleModelSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
