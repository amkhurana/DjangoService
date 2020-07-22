from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=80)
    author = serializers.CharField(max_length=200)
    email = serializers.EmailField(max_length=70)
    date = serializers.DateTimeField()

    def Create(self, validated_data):
        return Article.objects.Create(validated_data)

    def Create(self, instance, validated_data):
        instance.title = validated_data('title', instance.title)
        instance.author = validated_data('author', instance.author)
        instance.email = validated_data('email', instance.email)
        instance.date = validated_data('date', instance.date)
        instance.save()
        return instance

class ArticleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'author']
