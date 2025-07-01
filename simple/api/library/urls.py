from django.urls import path
from .views import CreateBookView, CreateAuthorView

urlpatterns = [
    path('create-book/', CreateBookView.as_view(), name='create-book'),
    path('create-author/', CreateAuthorView.as_view(), name='create-author'),
]
