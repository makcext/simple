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
    def get(self, request, id=None):
        if id is not None:
            author = Author.objects.get(id=id)
            serializer = self.serializer_class(author)
            return Response(serializer.data)
        else:
            queryset = Author.objects.all()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
