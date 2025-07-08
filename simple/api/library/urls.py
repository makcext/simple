from django.urls import re_path
from django.urls import include
from simple.api.library.views import AuthorListView
urlpatterns = [
    re_path(
        r"api/",
        include(
            ("simple.api.library.urls", "simple.api"),
            namespace="library-api",
               ),
            ),
]
