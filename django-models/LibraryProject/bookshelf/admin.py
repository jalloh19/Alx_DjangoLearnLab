from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Columns displayed in the list view
    list_display = ('title', 'author', 'publication_year')

    # Filters in the right sidebar
    list_filter = ('author', 'publication_year')

    # Search box on top
    search_fields = ('title', 'author')
