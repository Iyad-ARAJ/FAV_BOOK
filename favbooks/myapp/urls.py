from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login',views.login,name='login'),
    path('books',views.go_to_books,name='books'),
    path('books/addbook/', views.addbook, name='addbook'),
    path('books/<int:id>/', views.book_detail, name='book_detail'),
    path('books/<int:id>/edit', views.edit_book, name='edit_book'),
    path('books/delete', views.delete_book, name='delete_book'),
    path('books/<int:id>/favorite',views.favorite_book),
    path('books/<int:id>/unfavorite',views.unfavorite_book),
    # path('books/<int:id>/delete', views.delete_book, name='delete_book'),
    path('logout',views.logout,name='logout'),

]