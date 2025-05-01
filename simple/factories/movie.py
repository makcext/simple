import factory.django
from simple.models.models import Movie


class MovieFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Movie
