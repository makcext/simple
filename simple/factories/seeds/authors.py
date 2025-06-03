from simple.factories.author import AuthorFactory
from simple.models.models import Author


def seed_authors():
    """Seed database with essential authors."""
    AuthorFactory.create(
        first_name="Leo",
        last_name="Tolstoy",
        biography="Russian writer, master of realistic fiction",
        is_active=True,
    )
    AuthorFactory.create(
        first_name="Fyodor",
        last_name="Dostoevsky",
        biography="Russian novelist and philosopher",
        is_active=True,
    )
    return Author.objects.all()
