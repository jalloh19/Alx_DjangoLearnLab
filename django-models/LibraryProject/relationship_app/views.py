from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import UserProfile
from django.contrib import messages


from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
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
            # You might want to add a success message here
        else:
            # Handle invalid role
            pass
            
        return redirect('admin_view')  # Redirect back to admin view
        
    except User.DoesNotExist:
        # Handle user not found
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
            return redirect('home')  # Replace with your home view name
    else:
        form = UserCreationForm()
    
    return render(request, 'relationship_app/register.html', {'form': form})