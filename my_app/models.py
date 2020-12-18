from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2 or not postData['first_name'].isalpha():
            errors["first_name"] = "First name should be at least 2 characters and only letter"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    
            errors['email'] = "Invalid email address!"
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['email'] = 'email taken'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be longer than 8 characters'
        if postData['password'] != postData['confirm']:
            errors['confirm_password'] = 'Password does not match'
        return errors

    def login_validator(self, postData):
        errors = {}
        # check email in db  
        user_list = User.objects.filter(email=postData['email'])
        if len(user_list) == 0:
            errors['email'] = 'email not found'
        # check password
        elif not bcrypt.checkpw(postData['password'].encode(), user_list[0].hashed_password.encode()):
            errors['password'] = 'Password did not match'
        return errors

class WishManager(models.Manager):
    def wish_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name']='A wish must consist of at least 3 characters'
        if len(postData['desc']) < 3:
            errors['desc']='A description must be provided'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    hashed_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wish(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    wisher = models.ForeignKey(User, related_name="wishes", on_delete = models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name='favorites')
    granted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()




