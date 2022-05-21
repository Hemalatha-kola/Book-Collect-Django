from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Reader(models.Model):
    name = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('readers_detail', kwargs={'pk': self.id})


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.TextField(max_length=100)
    cost = models.IntegerField()
    readers = models.ManyToManyField(Reader)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'book_id': self.id})    


class Bookmark(models.Model):
    date = models.DateField('bookmark date')
    pagenumber = models.IntegerField()

    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
        return  f"{self.pagenumber} {self.date}"

    class Meta:
        ordering = ['-date']   

class Photo(models.Model):
    url = models.CharField(max_length=200)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for book_id: {self.book_id} @{self.url}"