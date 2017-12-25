from __future__ import unicode_literals

from django.db import models

from datetime import date, datetime

import bcrypt, re

# Create your models here.

class UserManager(models.Manager):
    
    def validate_login(self, post_data):
        errors = []
        # check DB for post_data['user_name']
        if len(self.filter(user_name=post_data['user_name'])) > 0:
            # check this user's password
            user = self.filter(user_name=post_data['user_name'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('user_name/password incorrect')
        else:
            errors.append('user_name/password incorrect')

        if errors:
            return errors
        return user

    def validate_registration(self, postData):
        errors=[]

        #check all fields for any input (no empty field)
        #loop through entire dictionary look for a single empty field
        for key, value in postData.iteritems():
            if len(value) < 1:
                errors.append("All fields are required to register.")
                break

        # check length of name fields
            if len(postData['name']) < 2 or len(postData['user_name']) < 2:
                errors.append("name/username fields must be at least 3 characters")

        # check length of name password
        if len(postData['password']) < 8:
            errors.append("password must be at least 8 characters")
        
        # check uniqueness of username
        if len(User.objects.filter(user_name=postData['user_name'])) > 0:
            errors.append("username already in use. Try a new username.")

        # check password == password_confirm
        if postData['password'] != postData['password_confirm']:
            errors.append("Try again passwords do not match.")

        # check valid hire date must be less than or equal to current date (today)
        entered_date = postData['hire_date']
        try:
            if entered_date >= datetime.now():
                errors.append("Please provide a valid date for hire date field")
        except:
            pass
        
        if not errors:
            # make our new user
            # hash password
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=postData['name'],
                user_name=postData['user_name'],
                hire_date = postData['hire_date'],
                password=hashed
            )
            return new_user
        return errors



class User(models.Model):
    name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    hire_date = models.DateField(default=datetime.now)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    objects=UserManager()

    def __str__(self):
        return self.user_name

class WishManager(models.Manager):
    def validate_Wish(self, form_data):
        errors = []

        if len(form_data['item']) < 3:
            errors.append('Item cannot be blank. Item must be at least 3 characters!!!')
        return errors

class Wish(models.Model):
    user = models.ForeignKey(User, related_name="wishes")
    item = models.CharField(max_length=255)
    wishers = models.ManyToManyField(User, related_name="items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()