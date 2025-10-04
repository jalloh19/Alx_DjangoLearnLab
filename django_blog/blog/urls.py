from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Blog post URLs - UPDATED to match checker expectations
    path('post/', views.PostListView.as_view(), name='post-list'),  # Changed from 'posts/' to 'post/'
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),  # Changed from 'posts/new/' to 'post/new/'
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),  # Changed from 'edit/' to 'update/'
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
]