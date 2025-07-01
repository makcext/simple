from rest_framework import serializers
from simple.api.v1.factories.seeds.authors import Author
from simple.api.v1.factories.seeds.books import Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
