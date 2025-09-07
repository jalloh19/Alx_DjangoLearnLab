from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Redirect the root URL to the 'list_books' URL
    path('', RedirectView.as_view(pattern_name='list_books', permanent=False)),
    path('', include('relationship_app.urls')),
]
