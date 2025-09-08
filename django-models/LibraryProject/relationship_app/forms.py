from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Book


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
        }