from django.contrib import admin
from .models import Book, Bookmark, Reader, Photo

# Register your models here.
admin.site.register(Book)
admin.site.register(Bookmark)
admin.site.register(Reader)
admin.site.register(Photo)