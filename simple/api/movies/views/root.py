from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView


from simple.api.movies.serializers.root import (
   MovieCategorySerializer,
   MovieCategoryFieldsSerializer,
   MovieSerializer,
)

from simple.models import Movie, MovieCategory


class MovieCategoryListView(APIView):

  serializer_class = MovieCategorySerializer
  parser_classes = [JSONParser, FormParser]

  @extend_schema(
      methods=["GET"],
      operation_id="movie-category-handler",
      description="Get all movie categories",
      tags=["Movies"],
      responses=MovieCategorySerializer,
  )

  def get(self, request):
    """
    Get all movie categories.
    """
    categories = MovieCategory.objects.all()
    serializer = self.serializer_class(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class MovieCategoryByIdView(APIView):
    """
    Retrieve a movie category by its ID.
    """

    serializer_class = MovieCategoryFieldsSerializer
    parser_classes = [JSONParser, FormParser]

    @extend_schema(
        methods=["GET"],
        operation_id="movie-category-by-id-handler",
        description="Get selected fields of movie category by ID",
        tags=["Movies"],
        responses={
            200: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the movie category",
                required=True,
            ),
        ],
    )
    def get(self, request, id):
        """
        Get selected fields of a movie category by its ID.
        """
        try:
            category = MovieCategory.objects.get(pk=id)
        except MovieCategory.DoesNotExist:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = MovieCategoryFieldsSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetActiveMovieView(APIView):
    serializer_class = MovieSerializer
    parser_classes = [JSONParser, FormParser]

    @extend_schema(
        methods=["GET"],
        operation_id="get-active-movie",
        description="Get first active movie and deactivate it",
        tags=["Movies"],
        responses={
            200: MovieSerializer,
            404: OpenApiTypes.OBJECT,
        },
    )
    def get(self, request):
        """
        Get first active movie and deactivate it.
        If no active movies left, returns "NO MOVIES".
        """
        movie = Movie.objects.filter(is_active=True).first()

        if not movie:
            return Response(
                {"message": "NO MOVIES"},
                status=status.HTTP_404_NOT_FOUND,
            )
        movie.is_active = False
        movie.save()

        serializer = self.serializer_class(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
