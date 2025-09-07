# CRUD Operations on Book Model

## 1. Create
```python
from bookshelf.models import Book

# Create a Book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
# <Book: 1984 by George Orwell (1949)>


# Retrieve all Book instances
Book.objects.all()
# <QuerySet [<Book: 1984 by George Orwell (1949)>]>

# Get the created book and update the title
book = Book.objects.get(id=1)
book.title = "Nineteen Eighty-Four"
book.save()
book
# <Book: Nineteen Eighty-Four by George Orwell (1949)>

# Delete the created book
book = Book.objects.get(id=1)
book.delete()
# (1, {'bookshelf.Book': 1})

# Confirm deletion
Book.objects.all()
# <QuerySet []>
