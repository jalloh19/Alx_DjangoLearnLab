```python
# Delete the book you created
from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
# Expected output: (1, {'bookshelf.Book': 1})

# Confirm deletion by retrieving all books
Book.objects.all()
# Expected output: <QuerySet []>

