```python
# Retrieve the book you just created
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.id, book.title, book.author, book.publication_year
# Expected output: (1, '1984', 'George Orwell', 1949)

