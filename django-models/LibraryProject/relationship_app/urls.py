from django.urls import path
from .views import list_books, LibraryDetailView, home_view
from .views import register_view, CustomLoginView, CustomLogoutView, home_view
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('home/', home_view, name='home'),
    path('books/', list_books, name='list_books'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]