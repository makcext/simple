from rest_framework import serializers
from simple.factories.seeds.authors import Author
from simple.factories.seeds.books import Book


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class AuthorFieldsSerializer(serializers.Serializer):
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


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    original_title = serializers.CharField(required=False, allow_blank=True)
    slug = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    publication_date = serializers.DateField()
    isbn = serializers.CharField(max_length=20)
    page_count = serializers.IntegerField(min_value=1)
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    author_name = serializers.CharField(source="author.full_name", read_only=True)
    is_active = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
