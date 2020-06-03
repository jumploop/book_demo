from django.contrib import admin
from books.models import Books


# Register your models here.

class BooksAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']
    ordering = ('name',)


admin.site.register(Books, BooksAdmin)
