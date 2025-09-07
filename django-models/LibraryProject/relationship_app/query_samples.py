import os
import sys


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

try:
    author1 = Author.objects.create(name="Stephen King")
    author2 = Author.objects.create(name="J.K. Rowling")

    book1 = Book.objects.create(title="The Shining", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Sorcerer's Stone", author=author2)
    book3 = Book.objects.create(title="It", author=author1)

    library1 = Library.objects.create(name="Central Library")
    library1.books.add(book1, book2)
    
    librarian1 = Librarian.objects.create(name="Alice Johnson", library=library1)
    
    print("Sample data created successfully.\n")

except Exception as e:
    print(f"Sample data already exists or an error occurred: {e}\n")



print("Query 1: All books by a specific author")
author_name = "Stephen King"
author = Author.objects.get(name=author_name)
books = Book.objects.filter(author=author)

for book in books:
    print(f"- {book.title}")
print("\n")



print("Query 2: All books in Central Library")
library_name = "Central Library"
central_library = Library.objects.get(name=library_name)
for book in central_library.books.all():
    print(f"- {book.title}")
print("\n")


#
print("Query 3: Librarian for Central Library")
library_name = "Central Library"
central_library = Library.objects.get(name=library_name)

# Find the librarian by filtering on the related library object
librarian = Librarian.objects.get(library=central_library)

print(f"- The librarian is {librarian.name}")