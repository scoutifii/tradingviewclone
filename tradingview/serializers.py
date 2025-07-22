from rest_framework import serializers
from .models import Post, Comment

class PostSerializers(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = '__all__'

class CommentSerializers(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'