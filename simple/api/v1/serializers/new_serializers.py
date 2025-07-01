from rest_framework import serializers
from simple.models.models import Movie, Author, Book


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "is_active",
            "created_at",
            "updated_at",
            "movies_count",
        ]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            "id",
            "first_name",
            "last_name",
            "biography",
            "birth_date",
            "death_date",
            "nationality",
            "is_active",
            "created_at",
            "updated_at",
            "books_count",
        ]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "original_title",
            "slug",
            "description",
            "publication_date",
            "isbn",
            "page_count",
            "author",
            "author_name",
            "is_active",
            "created_at",
            "updated_at",
        ]
