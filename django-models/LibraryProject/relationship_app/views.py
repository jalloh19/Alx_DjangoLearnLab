from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Library, UserProfile
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .forms import BookForm, CustomUserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

def home_view(request):
    return render(request, 'relationship_app/home.html')

def list_books(request):
    """
    Function-based view to display a list of all books.
    """
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

# Utility functions for role checking
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Role-based views
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

@login_required
@user_passes_test(is_admin)
def assign_role(request, user_id, role):
    """
    Admin view to assign roles to users
    """
    try:
        user = User.objects.get(id=user_id)
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Validate the role
        valid_roles = ['Admin', 'Librarian', 'Member']
        if role in valid_roles:
            user_profile.role = role
            user_profile.save()
            messages.success(request, f'Role {role} assigned to {user.username} successfully!')
        else:
            messages.error(request, 'Invalid role specified!')
            
        return redirect('admin_view')
        
    except User.DoesNotExist:
        messages.error(request, 'User not found!')
        return redirect('admin_view')

def register(request):
    """
    User registration view
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create UserProfile with default 'Member' role
            UserProfile.objects.create(user=user, role='Member')
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})


# Book List View
@login_required
@permission_required('relationship_app.can_view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})

# Add Book View
@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

# Edit Book View
@login_required
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

# Delete Book View
@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    return render(request, 'relationship_app/delete_book.html', {'book': book})

# View Book Detail
@login_required
@permission_required('relationship_app.can_view_book', raise_exception=True)
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'relationship_app/book_detail.html', {'book': book})

# Book management dashboard (combines list with action buttons)
@login_required
def book_management(request):
    books = Book.objects.all()
    can_add = request.user.has_perm('relationship_app.can_add_book')
    can_change = request.user.has_perm('relationship_app.can_change_book')
    can_delete = request.user.has_perm('relationship_app.can_delete_book')
    
    context = {
        'books': books,
        'can_add': can_add,
        'can_change': can_change,
        'can_delete': can_delete,
    }
    return render(request, 'relationship_app/book_management.html', context)