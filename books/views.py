from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from books.models import Books
from books.serializer import BooksSerializer


class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
