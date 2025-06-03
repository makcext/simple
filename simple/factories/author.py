import factory.django
from simple.models.models import Author


class AuthorFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Author
