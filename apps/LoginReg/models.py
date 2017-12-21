from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime, timedelta
import bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        # check DB for post_data['email']
        if len(self.filter(email=post_data['email'])) > 0:
            # check this user's password
            user = self.filter(email=post_data['email'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')

        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        errors = []

        #check all fields for any input (no empty field)
        #loop through entire dictionary look for a single empty field
        for key, value in post_data.iteritems():
            if len(value) < 1:
                errors.append("All fields are required")
                break

        # check length of name fields
        if len(post_data['first_name']) < 2 or len(post_data['last_name']) < 2:
            errors.append("name fields must be at least 3 characters")

        # check length of name password
        if len(post_data['password']) < 8:
            errors.append("password must be at least 8 characters")

        # check name fields for letter characters            
        if not re.match(NAME_REGEX, post_data['first_name']) or not re.match(NAME_REGEX, post_data['last_name']):
            errors.append('name fields must be letter characters only')

        # check emailness of email
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("invalid email")

        # check uniqueness of email
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors.append("email already in use")

        # check password == password_confirm
        if post_data['password'] != post_data['password_confirm']:
            errors.append("passwords do not match")
        # class datetime.timedelta
        # A duration expressing the difference between two date, time, or datetime instances to microsecond resolution.
        minage = timedelta(days=365*10)
        try:
            converted = datetime.strftime(post_data['birthday'], '%Y-%m-%d')
            print "converted", converted
            # check valid birthdate (year) must be less than current year
            if converted >= datetime.now():
                errors.append("Please provide a valid date for birthday field")
            # check birthdate for adult users 
            elif datetime.now() - converted < minage:
                errors.append("Must be over 16 to register")
        except:
            pass

        if not errors:
            # make our new user
            # hash password
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                first_name=post_data['first_name'],
                last_name=post_data['last_name'],
                email=post_data['email'],
                birthday = post_data['birthday'],
                password=hashed
            )
            return new_user
        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField(unique=True)
    password= models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

def __str__(self):
    return self.email
