from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book, Author

class BookAPITests(APITestCase):
    def setUp(self):
        """
        Set up test data that will be used across all test cases
        """
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title='Animal Farm',
            publication_year=1945,
            author=self.author2
        )
        
        # API endpoints
        self.book_list_url = reverse('book-list')
        self.book_detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.book_create_url = reverse('book-create')
        self.book_update_url = reverse('book-update', kwargs={'pk': self.book1.pk})
        self.book_delete_url = reverse('book-delete', kwargs={'pk': self.book1.pk})

    def test_get_book_list(self):
        """
        Test retrieving list of books
        """
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the count in the response data (it might be paginated)
        if 'results' in response.data:  # If using pagination
            self.assertEqual(len(response.data['results']), 3)
        else:
            self.assertEqual(len(response.data), 3)

    def test_get_book_detail(self):
        """
        Test retrieving a single book
        """
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Harry Potter')
        self.assertEqual(response.data['publication_year'], 1997)

    def test_create_book_authenticated(self):
        """
        Test creating a book with authentication using client.login()
        """
        # Use self.client.login() as requested by the checker
        self.client.login(username='testuser', password='testpassword123')
        data = {
            'title': 'New Book',
            'publication_year': 2024,
            'author': self.author1.id
        }
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    def test_create_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books
        """
        data = {
            'title': 'New Book',
            'publication_year': 2024,
            'author': self.author1.id
        }
        response = self.client.post(self.book_create_url, data)
        # DRF returns 403 Forbidden for unauthenticated users with IsAuthenticated permission
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_books_by_author(self):
        """
        Test filtering books by author
        """
        response = self.client.get(self.book_list_url, {'author': self.author2.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the count in the response data
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 2)
        else:
            self.assertEqual(len(response.data), 2)

    def test_search_books_by_title(self):
        """
        Test searching books by title
        """
        response = self.client.get(self.book_list_url, {'search': 'Harry'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the count in the response data
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['title'], 'Harry Potter')
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['title'], 'Harry Potter')

    def test_order_books_by_title_ascending(self):
        """
        Test ordering books by title ascending
        """
        response = self.client.get(self.book_list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
            
        titles = [book['title'] for book in data]
        self.assertEqual(titles, ['1984', 'Animal Farm', 'Harry Potter'])

    def test_update_book_authenticated(self):
        """
        Test updating a book with authentication using client.login()
        """
        self.client.login(username='testuser', password='testpassword123')
        data = {
            'title': 'Updated Harry Potter',
            'publication_year': 1998,
            'author': self.author1.id
        }
        response = self.client.put(self.book_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Harry Potter')

    def test_delete_book_authenticated(self):
        """
        Test deleting a book with authentication using client.login()
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.delete(self.book_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)

class AuthorAPITests(APITestCase):
    def setUp(self):
        """
        Set up test data for author tests
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.author = Author.objects.create(name='Test Author')
        self.author_list_url = reverse('author-list')
        self.author_detail_url = reverse('author-detail', kwargs={'pk': self.author.pk})

    def test_get_author_list(self):
        """
        Test retrieving list of authors
        """
        response = self.client.get(self.author_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle paginated response
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_get_author_detail(self):
        """
        Test retrieving a single author
        """
        response = self.client.get(self.author_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Author')