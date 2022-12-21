from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Note
from user.models import User
# Create your views here.


def note_present(request):
    if request.method == "GET":
        if request.GET:
            if 'title' in request.GET:
                show_note = Note.objects.get(title=request.GET['title'])
                dic = {"title": show_note.title, "content": show_note.content}
                return render(request, "note/present.html", dic)
            elif 'delete' in request.GET:
                del_note = Note.objects.get(title=request.GET['delete'])
                del_note.delete()
                return HttpResponseRedirect("/note/present")
        if request.session['username'] or request.COOKIES.get['username']:
            if request.session['username']:
                user_id = request.session['uid']
                username = request.session['username']
                notes = Note.objects.filter(user_id=user_id)

                if notes:
                    dic = {"username": username, "notes": notes}
                    return render(request, "note/present.html", dic)
                else:
                    return HttpResponse("<h1>Welcome, {0}</h1><h2>My Notes</h2><p><a href='/note/create'> you do not have any notes, go create one</a></p>".format(username))
            elif request.COOKIES.get['username']:
                user_id = request.COOKIES.get['uid']
                username = request.COOKIES.get['username']
                notes = Note.objects.filter(user_id=user_id)

                if notes:
                    dic = {"username": username, "notes": notes}

                    return render(request, "note/present.html", dic)
                else:
                    return HttpResponse("<h1>Welcome, {0}</h1><h2>My Notes</h2><p><a href='/note/create'> you do not have any notes, go create one</a></p>".format(username))
        else:
            return HttpResponseRedirect("/user/login")


def note_edit(request):
    if request.method == "GET":
        edit_note = Note.objects.get(title=request.GET["title"])
        dic = {"id": edit_note.id, "title": edit_note.title, "content": edit_note.content}
        return render(request, "note/edit.html", dic)
    elif request.method == "POST":
        note_id = request.POST['id']
        new_note = Note.objects.get(id=note_id)
        new_note.title=request.POST['title']
        new_note.content=request.POST['content']
        new_note.save()
        return HttpResponseRedirect("/note/present")


def note_create(request):
    if request.method == "GET":
        return render(request, "note/create.html")

    if request.method == "POST":
        if request.session['username'] or request.COOKIES.get['username']:
            if request.session['username']:
                user_id = request.session['uid']
                user = User.objects.get(id=user_id)
                if request.POST['title'] != '' and request.POST['content'] != '':
                    new_note = Note.objects.create(title=request.POST['title'], content=request.POST['content'],
                                                   user=user)
                    new_note.save()
                    return HttpResponseRedirect("/note/present")
                else:
                    return HttpResponse("<p> Your title or content is empty!</p><a href='/note/create'> Back </a>")
            elif request.COOKIES.get['username']:
                user_id = request.COOKIES.get['uid']
                user = User.objects.get(id=user_id)
                if request.POST['title'] != '' and request.POST['content'] != '':
                    new_note = Note.objects.create(title=request.POST['title'], content=request.POST['content'],
                                                   user=user)
                    new_note.save()
                    return HttpResponseRedirect("/note/present")
                else:
                    return HttpResponse("<p> Your title or content is empty!</p><a href='/note/create'> Back </a>")

        else:
            return HttpResponseRedirect("/user/login")

        #return HttpResponse(request.POST['content'])
