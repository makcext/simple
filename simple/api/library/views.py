from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from simple.factories.seeds.books import Book
from simple.factories.seeds.authors import Author


class CreateBookView(APIView):
    def post(self, request):
        try:
            Book.objects.create(**request.data)
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateAuthorView(APIView):
    def post(self, request):
        try:
            Author.objects.create(**request.data)
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
