from rest_framework import serializers
from simple.factories.seeds.authors import Author


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
