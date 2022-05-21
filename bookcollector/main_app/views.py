import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Book, Reader, Photo
from django.urls import reverse
from .forms import BookmarkForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


import logging
logging.basicConfig(level=logging.DEBUG)



    
# Create your views here.

def home(request):
    """
    home view
    http://localhostt:8000/

    """
    return render(request, 'home.html')

def about(request):
    """
    about view
    http://localhost:8000/about/

    """ 
    return render(request, 'about.html') 

@login_required
def books_index(request):
    """

    books index pages
    http://localhost:8000/books/

    """  
    logging.info('calling books_index')
    books = Book.objects.filter(user=request.user)

    return render(request, 'books/index.html', {'books' : books})

@login_required
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

@login_required
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

class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    #fields = '__all__'
    fields = ['title', 'author', 'genre', 'cost']

    def form_valid(self, form):   
        form.instance.user = self.request.user
        return super().form_valid(form)

class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['cost']     

    success_url = "/books/"   

class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    

    success_url = "/books/"    

@login_required
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

@login_required
def assoc_reader(request, book_id, reader_id):
  # Note that you can pass a toy's id instead of the whole toy object
    Book.objects.get(id=book_id).readers.add(reader_id)
    return redirect('detail', book_id=book_id)    

@login_required
def unassoc_reader(request, book_id, reader_id):
    Cat.objects.get(id=book_id).readers.remove(reader_id)
    return redirect('detail', book_id=book_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form' : form, 'error_message' : error_message}
    return render(request, 'registration/signup.html', context)      


class ReaderList(LoginRequiredMixin, ListView):
    model = Reader

class ReaderDetail(LoginRequiredMixin, DetailView):
    model = Reader

class ReaderCreate(LoginRequiredMixin, CreateView):
    model = Reader
    fields = '__all__'

class ReaderUpdate(LoginRequiredMixin, UpdateView):
    model = Reader
    fields = ['name']

class ReaderDelete(LoginRequiredMixin, DeleteView):
    model = Reader
    success_url = '/readers/'    
