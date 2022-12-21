from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import *
import hashlib

# Create your views here.


def reg_view(request):
    # get return the page
    if request.method == "GET":
        return render(request, 'user/register.html')
    # post examine the page
    elif request.method == 'POST':
        username = request.POST['username']
        password_1 = request.POST["password_1"]
        password_2 = request.POST['password_2']
        # check equality
        if password_1 != password_2:
            return HttpResponse("Your passwords are different, please retry")
        # hash code : non-reversible, md5 using
        m = hashlib.md5()
        m.update(password_1.encode())
        password_m = m.hexdigest()

        old_user = User.objects.filter(username=username)
        if old_user:
            return HttpResponse("Username already registered, try another one")

        try:
            user = User.objects.create(username=username, password=password_m)
        except Exception as e:
            print(e)
            return HttpResponse("Username already registered, try another one")

        # session storage
        request.session['username'] = username
        request.session['uid'] = user.id

        return HttpResponseRedirect("/user/login")


def login_view(request):
    if request.method == "GET":
        if 'logout' in request.GET:
            c_username = request.COOKIES.get('username')
            c_uid = request.COOKIES.get('uid')
            if c_uid and c_username:
                resp = HttpResponseRedirect('/user/login')
                resp.delete_cookie('username')
                resp.delete_cookie('uid')
                return resp
            if request.session.get('username') and request.session.get('uid'):
                del request.session['username']
                del request.session['uid']
                return HttpResponseRedirect('/user/login')

        # check login status, if session/cookie exists, go into index
        if request.session.get('username') and request.session.get('uid'):
            user = User.objects.get(username=request.session.get('username'))
            if user.email:
                return HttpResponseRedirect('/index?email=1')
            else:
                return HttpResponseRedirect('/index?email=0')
            # return HttpResponse('You are set')

        c_username = request.COOKIES.get('username')
        c_uid = request.COOKIES.get('uid')
        if c_uid and c_username:
            user = User.objects.get(username=c_username)
            if user.email:
                return HttpResponseRedirect('/index?email=1')
            else:
                return HttpResponseRedirect('/index?email=0')
            # return HttpResponse("You are set")

        # Session/cookies expire, or does not exist
        return render(request, "user/login.html")

    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)

        except Exception as e:
            print(e)
            return HttpResponse('Your username or password is wrong')

        # compare the password
        m = hashlib.md5()
        m.update(password.encode())

        if m.hexdigest() != user.password:
            return HttpResponse("Your username or password is wrong")

        # session storage
        request.session['username'] = username
        request.session['uid'] = user.id
        if user.email:
            resp = HttpResponseRedirect('/index?email=1')
        else:
            resp = HttpResponseRedirect('/index?email=0')
        if 'remember' in request.POST:
            resp.set_cookie('username', username, 3600*24*3)
            resp.set_cookie('uid', user.id, 3600*24*3)
        return resp
