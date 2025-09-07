from django.urls import path
from .views import list_books, LibraryDetailView, home_view

urlpatterns = [
    path('home/', home_view, name='home'),
    path('books/', list_books, name='list_books'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]