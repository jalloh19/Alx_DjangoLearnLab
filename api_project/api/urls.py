from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Router for CRUD
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Existing list-only view
    path('books/', BookList.as_view(), name='book-list'),

    # All CRUD routes from router
    path('', include(router.urls)),
]
