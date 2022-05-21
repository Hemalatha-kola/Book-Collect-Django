import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Book, Reader, Photo
from django.urls import reverse
from .forms import BookmarkForm


import logging
logging.basicConfig(level=logging.DEBUG)



    
# Create your views here.

def home(request):
    """
    home view
    http://localhostt:8000/

    """
    return HttpResponse("<h1>Hello World</h1>")

def about(request):
    """
    about view
    http://localhost:8000/about/

    """ 
    return render(request, 'about.html') 

def books_index(request):
    """

    books index pages
    http://localhost:8000/books/

    """  
    logging.info('calling books_index')
    books = Book.objects.all()

    return render(request, 'books/index.html', {'books' : books})

def books_detail(request, book_id):
    """
    book details page
    http://localhost:8000/books/1  
    """     
    logging.info('calling book_details')
    book = Book.objects.get(id=book_id)
    readers_book_doesnt_have = Reader.objects.exclude(id__in = book.readers.all().values_list('id'))
    bookmark_form = BookmarkForm()
    return render(request, 'books/detail.html', {'book':book, 'bookmark_form' : bookmark_form, 'readers' : readers_book_doesnt_have})

def add_photo(request, book_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, book_id=book_id)
        except:
            print('An error occured while uploading to s3')  
    return redirect("detail", book_id=book_id)

class BookCreate(CreateView):
    model = Book
    #fields = '__all__'
    fields = ['title', 'author', 'genre', 'cost']

    def get_success_url(self, **kwargs):
        return reverse('detail', args=(self.object.id,))    

class BookUpdate(UpdateView):
    model = Book
    fields = ['cost']     

    success_url = "/books/"   

class BookDelete(DeleteView):
    model = Book
    

    success_url = "/books/"    


def add_bookmark(request, book_id): 
    form = BookmarkForm(request.POST)
    # validate the form
    if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
        new_bookmark = form.save(commit=False)
        new_bookmark.book_id = book_id
        new_bookmark.save()
    return redirect('detail', book_id=book_id)

def assoc_reader(request, book_id, reader_id):
  # Note that you can pass a toy's id instead of the whole toy object
    Book.objects.get(id=book_id).readers.add(reader_id)
    return redirect('detail', book_id=book_id)    

