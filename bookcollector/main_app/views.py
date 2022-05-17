from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Book
from django.urls import reverse


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
    return render(request, 'books/detail.html', {'book':book})

class BookCreate(CreateView):
    model = Book
    fields = '__all__'

    def get_success_url(self, **kwargs):
        return reverse('detail', args=(self.object.id,))    

class BookUpdate(UpdateView):
    model = Book
    fields = ['cost']     

    success_url = "/books/"   

class BookDelete(DeleteView):
    model = Book
    

    success_url = "/books/"     