from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name="about"),
    path('books/', views.books_index, name='index'),
    path('books/<int:book_id>', views.books_detail, name='detail'),
    path('books/create', views.BookCreate.as_view(), name='books_create'),
    path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='books_update'),
    path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='books_delete'),
    path('books/<int:book_id>/add_bookmark/', views.add_bookmark, name='add_bookmark'),
    path('books/<int:book_id>/assoc_reader/<int:reader_id>/', views.assoc_reader, name='assoc_reader'),
    path('books/<int:book_id>/add_photo/', views.add_photo, name='add_photo'),
    path('books/<int:book_id>/unassoc_reader/<int:reader_id>/', views.unassoc_reader, name='unassoc_reader'),
    path('readers/', views.ReaderList.as_view(), name='readers_index'),
    path('readers/<int:pk>/', views.ReaderDetail.as_view(), name='readers_detail'),
    path('readers/create/', views.ReaderCreate.as_view(), name='readers_create'),
    path('readers/<int:pk>/update/', views.ReaderUpdate.as_view(), name='readers_update'),
    path('readers/<int:pk>/delete/', views.ReaderDelete.as_view(), name='readers_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]