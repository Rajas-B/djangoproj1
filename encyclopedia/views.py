from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
import markdown2
import random
from . import util

class NewPage(forms.Form):
    title = forms.CharField(label = "Title")
    content = forms.CharField(widget = forms.Textarea, label = "Content")

def index(request):
    if request.method=="POST":
        request.session["searchres"] = []
        request.session["searchq"] = request.POST.get('searchq')
        for page in util.list_entries():
            if page == request.session["searchq"]:
                return HttpResponseRedirect(reverse("entry", args=(page,)))
            elif request.session["searchq"] in page:
                request.session["searchres"].append(page)
        return render(request, "encyclopedia/index.html", {
            "entries": request.session["searchres"]
        })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def newpage(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            request.session["title"] = form.cleaned_data["title"]
            request.session["content"] = form.cleaned_data["content"]
            if util.get_entry(request.session["title"]) is None:
                util.save_entry(request.session["title"], request.session["content"])
            else:
                return render(request, "encyclopedia/newpage.html",{
                    "form": form, "error": "The title is taken"
                })
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/newpage.html",{
                "form": form, "error": ""
            })
    return render(request, "encyclopedia/newpage.html",{
        "form": NewPage(), "error": ""
    })
def entry(request, title):
    str1 = util.get_entry(title)
    str2 = markdown2.markdown(str1)
    return render(request,"encyclopedia/entry.html",{
        "content": str2, "title":title
    })

def edit(request, title):
    if request.method=="POST":
        request.session["content"] = request.POST.get('editcontent')
        util.save_entry(title, request.session["content"])
        return HttpResponseRedirect(reverse("entry", args=(title, )))
    request.session["title"]=title
    request.session["content"]=util.get_entry(title)
    return render(request, "encyclopedia/edit.html",{
        "title": title, "content": request.session["content"]
    })
def rand(request):
    ch = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", args=(ch,)))
