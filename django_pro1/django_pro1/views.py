from django.http import HttpResponse, HttpResponseRedirect
from django.core import mail
from user.models import User
from django.shortcuts import render
import random


def redirect(request):
    return HttpResponseRedirect('/index')


def test(request):
    if request.method == "POST":
        if 'email' in request.POST:
            if "@" in request.POST['email'] and "." in request.POST['email']:
                all_users = User.objects.all()
                for i in all_users:
                    if i.email == request.POST['email']:
                        return HttpResponse("Your Email has been registered, try another one")
                code = random.randint(100000, 999999)
                mail.send_mail(from_email="fu.servertester@gmail.com",
                               message="Hi! Welcome to Fu's server, your register code is {0}.".format(code),
                               recipient_list=[request.POST['email']],
                               subject="Your register code in Fu's server")
                dic = {"code": code, "email": request.POST['email']}
                return render(request, 'index/test.html', dic)

        else:
            if request.POST['code'] == request.POST['realcode']:
                user = User.objects.get(username=request.session['username'])
                user.email = request.POST['emailnow']
                user.save()
                return HttpResponseRedirect("/index?email=1")









