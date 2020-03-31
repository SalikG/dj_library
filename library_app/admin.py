from django.contrib import admin
from .models import Book, Magazine, BookLoan, Genre, Author, MagazineLoan

# Register your models here.

admin.site.register(Book)
admin.site.register(Magazine)
admin.site.register(BookLoan)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(MagazineLoan)

