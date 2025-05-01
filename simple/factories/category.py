import factory.django
from simple.models.models import MovieCategory


class MovieCategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = MovieCategory
