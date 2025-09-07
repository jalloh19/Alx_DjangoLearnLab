from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.shortcuts import render

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