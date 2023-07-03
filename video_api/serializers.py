from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Posts
from django.contrib.auth import authenticate

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']




# WriteOnly
class PostsSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()
    video_url = serializers.ReadOnlyField()
 
    class Meta:
        model = Posts
        fields = ['id', 'image_url', 'image', 'video_url','video', 'title', 'category']

    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation.pop("image")
        representation.pop("video")
        return representation
    
    
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']

# ReadOnly
class ReadPostsSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()
    video_url = serializers.ReadOnlyField()
    category = CategorySerializer()
    users = UserSerializer()

    class Meta:
        model = Posts
        fields = ['id', 'users', 'id', 'image_url', 'video_url', 'title', 'created','updated', 'category']



#------------------ FOR USER AUTHENTICATION ------------------#


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], None, validated_data['password'])
        return user


class UserSerializerr(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError("Invalid Details")
    
