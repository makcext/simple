from simple.factories.book import BookFactory
from simple.models.models import Book, Author


def seed_books():
    tolstoy = Author.objects.get(last_name="Tolstoy")
    dostoevsky = Author.objects.get(last_name="Dostoevsky")

    BookFactory.create(
        title="War and Peace",
        author=tolstoy,
        description="Epic novel about French invasion of Russia",
        is_active=True,
        slug="war-and-peace"
    )
    BookFactory.create(
        title="Crime and Punishment",
        author=dostoevsky,
        description="Novel about moral dilemmas",
        is_active=True,
        slug="crime-and-punishment"
    )
    return Book.objects.all()
