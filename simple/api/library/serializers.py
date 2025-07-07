from rest_framework import serializers
from simple.factories.seeds.authors import Author  # noqa: F401
from simple.factories.seeds.books import Book  # noqa: F401


class AuthorRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        return {
            "id": value.id,
            "first_name": value.first_name,
            "last_name": value.last_name
        }


class BookRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        return {
            "id": value.id,
            "title": value.title
        }


class AuthorItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    biography = serializers.CharField()
    birth_date = serializers.DateField()
    death_date = serializers.DateField(required=False, allow_null=True)
    nationality = serializers.CharField()
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class BookItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    original_title = serializers.CharField(required=False)
    slug = serializers.CharField()
    description = serializers.CharField()
    publication_date = serializers.DateField()
    isbn = serializers.CharField()
    page_count = serializers.IntegerField()
    author = AuthorRelatedField(read_only=True)
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def to_representation(self, instance):
        author_data = None
        if instance.author:
            author_data = (
                AuthorRelatedField().to_representation(instance.author)
            )

        return {
            "id": instance.id,
            "title": instance.title,
            "original_title": instance.original_title,
            "slug": instance.slug,
            "description": instance.description,
            "publication_date": instance.publication_date,
            "isbn": instance.isbn,
            "page_count": instance.page_count,
            "author": author_data,
            "is_active": instance.is_active,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at
        }


class AuthorWithBooksSerializer(serializers.Serializer):
    author = AuthorItemSerializer()
    books = serializers.ListField(
        child=BookRelatedField(read_only=True)
    )

    def to_representation(self, instance):
        author_serializer = AuthorItemSerializer(instance['author'])
        books_data = [
            BookRelatedField().to_representation(book)
            for book in instance['books']
        ]

        return {
            "author": author_serializer.data,
            "books": books_data,
        }
