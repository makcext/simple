from simple.factories.category import MovieCategoryFactory
from simple.models.models import MovieCategory


def seed_categories():
    MovieCategoryFactory.create(
        name="Action",
        description="Action movies",
        slug="action",
        is_active=True,
    )
    MovieCategoryFactory.create(
        name="Adventure",
        description="Adventure movies",
        slug="adventure",
        is_active=True,
    )
    MovieCategoryFactory.create(
        name="Comedy",
        description="Comedy movies",
        slug="comedy",
        is_active=True,
    )
    MovieCategoryFactory.create(
        name="Drama",
        description="Drama movies",
        slug="drama",
        is_active=True,
    )
    MovieCategoryFactory.create(
        name="Fantasy",
        description="Fantasy movies",
        slug="fantasy",
        is_active=True,
    )
    MovieCategoryFactory.create(
        name="Horror",
        description="Horror movies",
        slug="horror",
        is_active=True,
    )
    MovieCategoryFactory.create(
        name="Mystery",
        description="Mystery movies",
        slug="mystery",
        is_active=True,
    )

    return MovieCategory.objects.all()
