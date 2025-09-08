from django.urls import path
from .views import list_books, LibraryDetailView, home_view
from .views import register_view, CustomLoginView, CustomLogoutView, home_view
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from django.urls import path
from . import views

urlpatterns = [
    # Home and authentication URLs
    path('', views.home_view, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    
    # Role-based access URLs
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    path('assign-role/<int:user_id>/<str:role>/', views.assign_role, name='assign_role'),
    
    # Book management URLs (ADD THESE)
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),  # ← This one was missing
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),  # ← This one was missing
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('books/management/', views.book_management, name='book_management'),
    
    # Your existing book/library URLs
    path('list-books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
]