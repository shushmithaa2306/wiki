from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
from django.http import Http404
from django import forms
import markdown2
import random

from . import util

class Search(forms.Form):
    query=forms.CharField()

class newPage(forms.Form):
    title=forms.CharField(label="Add title")
    content=forms.CharField(label="Add your content",widget=forms.Textarea)

class EditForm(forms.Form):
    content=forms.CharField(label="Add your content",widget=forms.Textarea)



def index(request):
    return render(request, "encyclopedia/index.html", {
        "title":"Encyclopedia",
        "entries": util.list_entries(),
        "form":Search()
    })

def edit(request,name):
    if request.method == 'GET':
        page = util.get_entry(name)
        return render(request, "encyclopedia/edit.html", {
        "form": Search(),
        "editPageform": EditForm(initial={'content':page})
        })
    else:
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(name, content)
            page = util.get_entry(name)
            converted_page = markdown2.markdown(page)
            return render(request,"encyclopedia/entryPage.html",{
            "title":name.capitalize(),
            "convertedpage":converted_page,
            "form":Search()
        })



def entryPage(request,name):
    entries=util.list_entries()
    page=util.get_entry(name)
    if name in entries:
        converted_page=markdown2.markdown(page)
        return render(request,"encyclopedia/entryPage.html",{
            "title":name.capitalize(),
            "convertedpage":converted_page,
            "form":Search()
        })
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def newpage(request):
    if request.method=="POST":
        form=newPage(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["content"]
            entries=util.list_entries()
            if title in entries:
                return HttpResponseNotFound('<h1> Page already exists </h1>')
            else:
                util.save_entry(title,content)
                save_page = util.get_entry(title)
                convert_page=markdown2.markdown(save_page)
                return render(request,"encyclopedia/entryPage.html",{
                    "title":title.capitalize(),
                    "convertedpage":convert_page,
                    "form":Search()
                })
    else:
        return render(request,"encyclopedia/newpage.html",{
            "form":Search(),
             "newPageform":newPage()
        })


def search(request):
    if request.method=="POST":
        searchform=Search(request.POST) 
        searched = []
        if searchform.is_valid():
            query=searchform.cleaned_data["query"]
            entries=util.list_entries()
            for entry in entries:
                if entry == query:
                    page = util.get_entry(entry)
                    cpage = markdown2.markdown(page)
                    return render(request,"encyclopedia/entryPage.html",{
                        "title":entry,
                        "convertedpage":cpage,
                        "form":Search()
                    })
                if query.lower() in entry.lower():
                    searched.append(entry)
            if searched:
                return render(request, "encyclopedia/index.html",{
                    "titles":"Encyclopedia",
                    "entries":searched,
                    "form":Search()
                })
            else:
                return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
                return HttpResponseNotFound('<h1>Page not found</h1>')
def randompage(request):
    entries=random.choice(util.list_entries())
    save_page = util.get_entry(entries)
    convert_page=markdown2.markdown(save_page)
    return render(request,"encyclopedia/entryPage.html",{
        "title":"Encyclopedia",
        "convertedpage":convert_page,
        "form":Search()
    })
    

