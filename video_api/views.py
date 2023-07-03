from rest_framework.generics import(ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Posts, Category
from rest_framework import filters
from .serializers import(PostsSerializer,
                         LoginUserSerializer,
                        CategorySerializer, 
                        ReadPostsSerializer, 
                        RegisterSerializer, 
                        UserSerializer,
                        UserSerializerr)
from rest_framework import status
from.permissions import IsAuthorOrReadOnly
from django.contrib.auth import login
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
# import cloudinary.api





class CategoryView(viewsets.ModelViewSet):
    """The Category View inherits from ModelViewset that provides all types of http request actions."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostSearch(generics.ListAPIView):
    """The PostSearch allows for searching names and titles relating to the Posts instance"""
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = (TokenAuthentication, )
    queryset = Posts.objects.all()
    serializer_class = ReadPostsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title', 'category__name', 'users__username']





class PostListCreateView(ListCreateAPIView):
    '''Allows authenticated users to make a post and to see all post'''
    permission_classes = [IsAuthorOrReadOnly, ]
    authentication_classes = (TokenAuthentication, )
    queryset = Posts.objects.all()
    serializer_class = ReadPostsSerializer

    def post(self, request, format=None):
        serializer = PostsSerializer(data=request.data)
        
        # if the new serialized post is valid, then save
        if serializer.is_valid():
            serializer.validated_data['users'] = request.user # This line checks if the user is authorized to make a post
            post = serializer.save()

            image_url = post.image.url
            video_url = post.video.url

            category_serializer = CategorySerializer(post.category)
            
            user_serializer = UserSerializer(request.user)


            post.save()
            data = {
                'user': user_serializer.data,
                'id': post.id,
                'title': post.title,
                'video': video_url,
                'image': image_url,
                'category': category_serializer.data,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



class PostDetailView(RetrieveUpdateDestroyAPIView):
    """Allows authenticated users to get specific post,
    and also get a specific post to update or delete"""
    permission_classes = (IsAuthorOrReadOnly, )
    authentication_classes = (TokenAuthentication,)
    queryset = Posts.objects.all()
    serializer_class = ReadPostsSerializer
    lookup_field = 'id'




    def patch(self, request, id, *args, **kwargs):
        post = self.get_object()
        serializer = PostsSerializer(post, data=request.data)
        
        # if the new serialized post is valid, then save
        if serializer.is_valid():

            post = serializer.save()

            image_url = post.image.url
            video_url = post.video.url

            category_serializer = CategorySerializer(post.category)
            user_serializer = UserSerializer(request.user)

            post.save()
            data = {
                'user': user_serializer.data,
                'id': post.id,
                'title': post.title,
                'video': video_url,
                'image': image_url,
                'category': category_serializer.data
            }

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def delete(self, request, *args, **kwargs):
    #     post = self.get_object()
    #     post_delete = post.image.url.public_id, post.video.url.public_id
    #     cloudinary.api.delete_resources(post_delete)
    #     post.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)







#---------------USER AUTHENTICATION----------------------#


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            return Response({
                'user': UserSerializerr(user, context=self.get_serializer_context()).data,
                'token': AuthToken.objects.create(user)[1]
            })
        
    


class LoginView(KnoxLoginView):
    permission_classes = ()
    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = (TokenAuthentication, )
    serializer_class = UserSerializerr

    def get_object(self):
        return self.request.user

