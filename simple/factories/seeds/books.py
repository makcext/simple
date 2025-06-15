from datetime import date
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
        slug="war_and_peace",
        publication_date=date(1869, 1, 1),
        isbn='978-0199232765',
        page_count=1225,
    )
    BookFactory.create(
        title="Crime and Punishment",
        author=dostoevsky,
        description="Novel about moral dilemmas",
        is_active=True,
        slug="crime_and_punishment",
        publication_date=date(1866, 1, 1),
        isbn='978-0486415871',
        page_count=430,
    )

    BookFactory.create(
        title="Anna Karenina",
        author=tolstoy,
        description="Tragic novel about love and society",
        is_active=True,
        slug="anna_karenina",
        publication_date=date(1878, 1, 1),
        isbn='978-0143035008',
        page_count=864,
    )
    BookFactory.create(
        title="The Idiot",
        author=dostoevsky,
        description="Novel about a truly good man",
        is_active=False,
        slug="the_idiot",
        publication_date=date(1869, 1, 1),
        isbn='978-0375702242',
        page_count=656,
    )
    BookFactory.create(
        title="Resurrection",
        author=tolstoy,
        description="Novel about moral redemption",
        is_active=True,
        slug="resurrection",
        publication_date=date(1899, 1, 1),
        isbn='978-0192831115',
        page_count=492,
    )

    return Book.objects.all()
