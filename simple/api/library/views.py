from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import logging

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)

from simple.factories.seeds.authors import Author
from simple.factories.seeds.books import Book

from .serializers import (
    AuthorItemSerializer,
    BookItemSerializer,
    AuthorWithBooksSerializer
)


logger = logging.getLogger(__name__)


class AuthorListView(APIView):
    """
    API endpoint for listing and creating authors
    """
    serializer_class = AuthorItemSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='active_only',
                type=bool,
                location=OpenApiParameter.QUERY,
                description='Filter only active authors',
                required=False
            )
        ],
        examples=[
            OpenApiExample(
                'Author List Example',
                value=[{
                    "id": 1,
                    "first_name": "John",
                    "last_name": "Doe"
                }],
                response_only=True
            )
        ]
    )
    def get(self, request):
        try:
            queryset = Author.objects.all()
            if request.query_params.get('active_only', '').lower() == 'true':
                queryset = queryset.filter(is_active=True)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching authors: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        request=AuthorItemSerializer,
        examples=[
            OpenApiExample(
                'Create Author Example',
                value={
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "biography": "Famous writer"
                },
                request_only=True
            )
        ]
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorDetailView(APIView):
    serializer_class = AuthorItemSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='Author ID'
            )
        ]
    )
    def get(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
            serializer = self.serializer_class(author)
            return Response(serializer.data)
        except Author.DoesNotExist:
            return Response(
                {"error": "Author not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class BookListView(APIView):
    serializer_class = BookItemSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='author_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Filter books by author ID',
                required=False
            )
        ],
        examples=[
            OpenApiExample(
                'Book List Example',
                value=[{
                    "id": 1,
                    "title": "Sample Book",
                    "author": {
                        "id": 1,
                        "first_name": "John",
                        "last_name": "Doe"
                    }
                }],
                response_only=True
            )
        ]
    )
    def get(self, request):
        try:
            queryset = Book.objects.all()
            author_id = request.query_params.get('author_id')
            if author_id:
                queryset = queryset.filter(author_id=author_id)
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching books: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AuthorBooksView(APIView):
    serializer_class = AuthorWithBooksSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='author_id',
                type=int,
                location=OpenApiParameter.PATH,
                description='Author ID'
            )
        ],
        examples=[
            OpenApiExample(
                'Author Books Example',
                value={
                    "author": {
                        "id": 1,
                        "first_name": "John",
                        "last_name": "Doe"
                    },
                    "books": [
                        {
                            "id": 1,
                            "title": "Sample Book"
                        }
                    ]
                },
                response_only=True
            )
        ]
    )
    def get(self, request, author_id):
        try:
            author = Author.objects.get(pk=author_id)
            serializer = self.serializer_class({
                'author': author,
                'books': Book.objects.filter(author=author)
            })
            return Response(serializer.data)
        except Author.DoesNotExist:
            return Response(
                {"error": "Author not found"},
                status=status.HTTP_404_NOT_FOUND
            )
