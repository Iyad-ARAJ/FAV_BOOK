from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def validate_registration(self,postData):
        errors = {}
        if len(postData['firstname']) < 2 :
            errors['firstname'] ='FIRST  name must be at least 2 char'
        if len(postData['lastname']) < 2:
            errors['lastname'] = 'Last name must be at least 2 char'
            #validate the email
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if User.objects.filter(email=postData['email']).exists():
            errors['email'] = "Email already in use!"
            #validate the password
        if len(postData['password']) < 6:
            errors['password'] = 'Password must be at least 6 char'
        if len(postData['password']) != len(postData['confirm_password']):
            errors['password'] = 'Password do not match'
        
        return errors
    
class BookManager(models.Manager):
    def validate_book(self,postData):
        errors = {}
        if len(postData['title']) == 0 :
            errors['title'] = 'Tile is required'
        if len(postData['desc']) < 5 :
            errors['desc'] = 'dec must be al least 5'
        return errors


class User(models.Model):
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc  = models.TextField()
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_books")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = BookManager()

def create_user(post):
    password = post['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return User.objects.create(firstname = post['firstname'],lastname=post['lastname'],email = post['email'] ,password= pw_hash)

def create_book(post, uploaded_by):
    return Book.objects.create(
        title=post['title'],
        desc=post['desc'],
        uploaded_by=uploaded_by  # Assign the uploaded_by user here
    )
def add_user_to_book(user,book): 
    book=book.users_who_like.add(user)

def remove_user_from_book(user,book):
    book = book.users_who_like.remove(user)

def get_userid(id):
    return User.objects.get(id = id)


def get_bookid(id):
    return Book.objects.get(id = id)

def get_all_books():
    return Book.objects.all()

def filter_email(post):
    return User.objects.filter(email = post['email'])

def update_book(post,id):
    book = get_bookid(id)
    book.title = post['title']
    book.desc = post['desc']
    book.save()

def delete_book1(POST):
  book_remove=get_bookid(POST['book_id'])
  book_remove.delete()


