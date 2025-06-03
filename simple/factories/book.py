import factory.django
from simple.models.models import Book


class BookFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Book
