from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, FormParser

from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)

from simple.models import Author
from simple.api.library.serializers.root import AuthorItemSerializer


class AuthorListView(APIView):
    """
    API endpoint for listing and creating authors
    """
    serializer_class = AuthorItemSerializer
    parser_classes = [JSONParser, FormParser]

    @extend_schema(
        methods=["GET"],
        operation_id="author-list-handler",
        description="Get all authors",
        tags=["Library"],
        responses={
            200: AuthorItemSerializer(many=True),
        },
        examples=[
            OpenApiExample(
                'Author List Example',
                value=[{
                    "id": 1,
                    "first_name": "John",
                    "last_name": "Doe",
                    "biography": "Famous author",
                    "birth_date": "1970-01-01",
                    "death_date": None,
                    "nationality": "American",
                    "is_active": True,
                    "created_at": "2025-01-01T00:00:00Z",
                    "updated_at": "2025-01-01T00:00:00Z"
                }],
                response_only=True
            )
        ]
    )
    def get(self, request, id=None):
            author = Author.objects.all()
            serializer = self.serializer_class(author, many=True)
            return Response(serializer.data)
