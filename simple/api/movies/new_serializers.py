from rest_framework import serializers
from simple.models import MovieCategory


class MovieCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieCategory
        fields = '__all__'
