from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from simple.models.models import Author
from simple.models.models import Book
from simple.api.library.serializers.root import (
    AuthorSerializer,
    AuthorFieldsSerializer,
    BookSerializer
)


class AuthorListView(APIView):
    """
    API endpoint for authors
    """
    serializer_class = AuthorSerializer
    parser_classes = [JSONParser, FormParser]

    @extend_schema(
        methods=["GET"],
        operation_id="author-handler",
        description="Get all authors",
        tags=["Authors"],
        responses=AuthorSerializer(many=True),
    )
    def get(self, request):
        """
        Get all authors with basic information
        """
        authors = Author.objects.all()
        serializer = self.serializer_class(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthorByIdView(APIView):
    """
    Retrieve an author by its ID with all fields.
    """
    serializer_class = AuthorFieldsSerializer
    parser_classes = [JSONParser, FormParser]

    @extend_schema(
        methods=["GET"],
        operation_id="author-by-id-handler",
        description="Get all fields of author by ID",
        tags=["Authors"],
        responses={
            200: AuthorFieldsSerializer,
            404: OpenApiTypes.OBJECT,
        },
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the author",
                required=True,
            ),
        ],
    )
    def get(self, request, id):
        """
        Get all fields of an author by ID
        """
        try:
            author = Author.objects.get(pk=id)
            serializer = AuthorFieldsSerializer(author)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Author.DoesNotExist:
            return Response(
                {"detail": "Author not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class AuthorBooksView(APIView):
    """
    Retrieve all books of an author by author ID.
    """
    serializer_class = BookSerializer
    parser_classes = [JSONParser, FormParser]

    @extend_schema(
        methods=["GET"],
        operation_id="author-books-handler",
        description="Get all books of author by author ID",
        tags=["Authors"],
        responses={
            200: BookSerializer(many=True),
            404: OpenApiTypes.OBJECT,
        },
        parameters=[
            OpenApiParameter(
                name="author_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the author",
                required=True,
            ),
        ],
    )
    def get(self, request, author_id):
        """
        Get all books of an author by author ID
        """
        try:
            author = Author.objects.get(pk=author_id)
            books = Book.objects.filter(author=author)
            serializer = self.serializer_class(books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Author.DoesNotExist:
            return Response(
                {"detail": "Author not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
