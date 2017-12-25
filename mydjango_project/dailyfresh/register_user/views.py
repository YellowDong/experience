from django.shortcuts import render, redirect
from .models import *
from hashlib import sha1


def register(request):
    return render(request, 'register_user/register.html')


def register_handle(request):
    post = request.POST
    username = post.get('user_name')
    pwd = post.get('pwd')
    cpwd = post.get('cpwd')
    email = post.get('email')
    if pwd != cpwd:
        return redirect('/register/')
    s = sha1()
    s.update(cpwd)
    s1 = s.hexdigest()
    user = UserInfo()
    user.username = username
    user.password = s1
    user.email = email
    user.save()
    return redirect('/register/login/')