import re
from django.shortcuts import render
from django import forms
from . import util
import encyclopedia
import random

class NewPageForm(forms.Form):
    entry_name = forms.CharField(widget=forms.TextInput(attrs={"style": "width: 25vw;", "class": "form-control"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"style": "width: 99%;", "class": "form-control"}))

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"style": "width: 99%;", "class": "form-control"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def page(request, name):
    if name in util.list_entries():
        return render(request, "encyclopedia/page.html", {
            "content": util.convert_md(util.get_entry(name)),
            "name": name,
            })
    else:
        return render(request, "encyclopedia/nopagefound.html")

def search(request):
    name = request.GET['q']
    if name in util.list_entries():
        return page(request, name)
    else:
        entries = [string for string in util.list_entries() if name in string]
        if not entries:
            return render(request, "encyclopedia/search.html", {
            "empty": True
        })
        return render(request, "encyclopedia/search.html", {
            "entries": entries,
            "empty": False
        })

def new_page(request):

    # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as a form
        form = NewPageForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the name and content from the "cleaned" version of form data
            name = form.cleaned_data["entry_name"]
            content = form.cleaned_data["content"]

            # Check if file already exists
            if name in util.list_entries():
                print("Entry already exists")
                return render(request, "encyclopedia/newpage.html", {
                    "form": NewPageForm(),
                    "error": True
                })
            else:
                # Create markdown file using data
                util.save_entry(name,content)

                # Redirect user to new entry page
                return page(request,name)

    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm(),
        "error": False
    })

def edit(request, name):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(name,content)
            return page(request,name)

    else:    
        content = util.get_entry(name)
        form = EditPageForm(initial={"content": content})
        return render(request, "encyclopedia/edit.html", {
            "name": name,
            "form": form
        })

def random_page(request):
    entry = random.choice(util.list_entries())
    return page(request,entry)
