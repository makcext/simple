from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieCategorySerializer
from simple.models import MovieCategory


class MovieCategoryHandler(APIView):
    def get(self, request):
        categories = MovieCategory.objects.all()
        serializer = MovieCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieCategoryByIdHandler(APIView):
    def get(self, request, id):
        try:
            category = MovieCategory.objects.get(pk=id)
            serializer = MovieCategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MovieCategory.DoesNotExist:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )
