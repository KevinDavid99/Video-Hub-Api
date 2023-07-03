from django.urls import path, include
from rest_framework import routers
from video_api import views
from knox import views as knox_views

router = routers.DefaultRouter()
router.register(r'category_post', views.CategoryView)
# router.register('register', views.RegisterView, 'register')
# router.register(r'post_items', views.PostList)

# urlpatterns = [
#     path('api/', views.PostList.as_view()),
#     path('cat_api/', views.CategoryList.as_view()),
#     path('allpost/<int:pk>/', views.PostDetail.as_view())
# ]

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/post_items/', views.PostListCreateView.as_view()),
    path('api/post_items/search/', views.PostSearch.as_view()),
    path('api/post_items/<int:id>/', views.PostDetailView.as_view()),
    path('api/register/', views.RegisterView.as_view()),
    path('api/login/', views.LoginView.as_view()),
    path('api/user/', views.UserAPI.as_view()),
    path('api/logout/', knox_views.LogoutView.as_view()),
    path('api/auth/', include('knox.urls')) 
]
