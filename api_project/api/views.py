from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
