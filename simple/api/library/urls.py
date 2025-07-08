from django.urls import path
from simple.api.library.views import AuthorListView

urlpatterns = [
    path(
        r"^api/author/$",
        AuthorListView.as_view(),
        name="author-list",
        ),
]
