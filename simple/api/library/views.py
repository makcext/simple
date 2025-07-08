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
from simple.api.library.serializers import AuthorItemSerializer


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
    def get(self, request):
        queryset = Author.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

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
