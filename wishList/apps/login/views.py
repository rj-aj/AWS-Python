# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User, Wish
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from datetime import datetime

# Create your views here.
def index(request):
    return render(request, 'login/index.html')

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect('/dashboard')
    

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully logged in!")
    return redirect('/dashboard')

def logout(request):
    if 'user_id' in request.session:
        request.session.delete()
    return redirect('/')

def dashboard(request):
    if 'user_id' in request.session:
        user = currentUser(request)
        wishes = Wish.objects.all()
        my_wishes = user.items.all()
        wishes = Wish.objects.exclude(id__in=my_wishes)

        context = {
        "user" : user,
        "wishes" : wishes,
        "my_wishes" : my_wishes,
        }
    return render(request, 'login/dashboard.html', context)

def addItem(request):
    if 'user_id' in request.session:
        user = currentUser(request)

        context = {
        "user" : user,
        }

    return render(request, 'login/addItem.html', context)

def submitItem(request):
    if request.method == 'POST':
        errors = Wish.objects.validate_Wish(request.POST)

        if not errors:
            user = currentUser(request)
            wish = Wish.objects.create(item=request.POST['item'], user=user)
            user.items.add(wish)
            return redirect('/dashboard')
        for error in errors:
            messages.error(request, error)

        return redirect('/addItem')
    return redirect('/dashboard')

def addWish(request, id):
    if 'user_id' in request.session:
        user = currentUser(request)
        wish = Wish.objects.get(id=id)
        wish.wishers.add(user)
        return redirect('/dashboard')

def removeWish(request, id):
    if 'user_id' in request.session:
        user = currentUser(request)
        wish = Wish.objects.get(id=id)
        wish.wishers.remove(user)
        return redirect('/dashboard')

def item(request, id):
    if 'user_id' in request.session:
        user = currentUser(request)

        context = {
        'user' : user,
        'wish' : Wish.objects.get(id=id)
        }
    return render(request, 'login/item.html', context)

def currentUser(request):
    user = User.objects.get(id=request.session['user_id'])
    return user

def delete(request, id):
    wish = Wish.objects.get(id=id)
    wish.delete()

    return render(request, '/dashboard')