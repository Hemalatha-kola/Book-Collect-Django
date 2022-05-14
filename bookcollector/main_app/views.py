from django.shortcuts import render
from django.http import HttpResponse


import logging
logging.basicConfig(level=logging.DEBUG)

class Book:  # Note that parens are optional if not inheriting from another class
    def __init__(self, title, author, genre, cost):
        self.title = title
        self.author = author
        self.genre = genre
        self.cost = cost

books = [
    Book('The Alchemist', 'Paulo Coelho', 'Adventure fiction', 50),
    Book('The Da Vinci Code', 'Dan Brown', 'Conspiracy fiction', 80),
    Book('Courage', 'Osho', 'psychology', 40)
]

    
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
    http://localhostt:8000/about/

    """ 
    return render(request, 'about.html') 

def books_index(request):
    """

    cats index pages
    http://localhost:8000/books/

    """  
    logging.info('calling books_index')

    return render(request, 'books/index.html', {'books' : books})