from django.shortcuts import render
from user.models import User
# Create your views here.


def index_view(request):
    if request.method == "GET":
        if 'email' in request.GET:
            if request.GET['email'] == '1':
                dic = {"email": True}
            else:
                dic = {"email": False}
            return render(request, 'index/index.html', dic)
        else:
            return render(request, 'index/index.html')
