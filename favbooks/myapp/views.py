from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages

def index(request):
    return render(request,'index.html')

#  to validate the the inputs fields , and if there's not any, create a user and save its ID in a session
def register(request):
    if request.method == 'POST':
        errors = User.objects.validate_registration(request.POST)
        if errors:
            for error in errors.values():
                messages.error(request,error)
            return redirect('/')
        
        #if there is no errors in inputs, create a user and save it in session
        user = create_user(request.POST)
        request.session['user_id'] = user.id
        return redirect('/books')
    else:
        # return render(request,'index.html')
        return redirect('/books')

def login(request):
    if request.method == 'POST':
        user = filter_email(request.POST)
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/books')
            else:
                messages.error(request, 'invalid  passwword or email')
                return redirect('/')
                
        else:
            messages.error(request, "Invalid Inputs")
            return redirect('/')

def go_to_books(request):                       
    if 'user_id' not in request.session :
        return redirect('/')
    user = get_userid(request.session['user_id'])
    allbooks = get_all_books()
    context = {
            'user' : user,
            'allbooks' : allbooks,
        }
    return render(request,'books.html',context)

def addbook(request):
    if request.method == 'POST':
        errors = Book.objects.validate_book(request.POST)
        if errors:
            for error in errors.values():
                messages.error(request,error)
            return redirect('/books')
        if 'user_id' not in request.session:
            return redirect('/')
        
        user = get_userid(request.session['user_id'])
        book = create_book(request.POST, uploaded_by=user)
        add_user_to_book(user,book)

        return redirect('/books')

def book_detail(request,id):
    if 'user_id' not in request.session:
        return redirect('/')
    book = get_bookid(id)
    user = get_userid(request.session['user_id'])
    context = {
        'book': book,
        'user':user
    }
    return render(request,'book_detail.html',context)
    
    
def edit_book(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = get_userid(request.session['user_id'])
    book = get_bookid(id)
    if request.method == 'POST':
        update_book(request.POST,id)
        return redirect(f'/books/{book.id}')
    return render(request,'edit_book.html',{'book':book})

def  delete_book(request):
  if request.method =='POST':
    delete_book1(request.POST)
    return redirect('/books')
  
def logout(request):
    request.session.clear()
    return redirect('/')

def favorite_book(request,id):
    user = get_userid(request.session['user_id'])
    book = get_bookid(id)
    add_user_to_book(user,book)
    return redirect(f'/books/{id}')

def unfavorite_book(request,id):
    user = get_userid(request.session['user_id'])
    book = get_bookid(id)
    remove_user_from_book(user,book)
    return redirect(f'/books/{id}')


