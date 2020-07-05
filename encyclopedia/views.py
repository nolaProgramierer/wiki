from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from . import util
from random import randint
from markdown2 import markdown


class NewEntryForm(forms.Form):
    title = forms.CharField(
        label="Title", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    entry = forms.CharField(
        label="Create Entry", widget=forms.Textarea(attrs={"class": "form-control"})
    )


class EditEntryForm(forms.Form):
    title = forms.CharField(
        label="Title", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    entry = forms.CharField(
        label="Edit Entry", widget=forms.Textarea(attrs={"class": "form-control"})
    )


# GET request in form returns query result
# or the GET request returns list of all encyclopedia entries
def index(request):
    query = request.GET.get("q")
    if util.get_entry(query):
        return render(
            request, "encyclopedia/entry.html", {"entries": util.get_entry(query)}
        )
    # Check incomplete, inexact and case insensitive GET query
    elif util.get_entry(query) is not query:
        entrylist = []
        for entry in util.list_entries():
            if query.casefold() in entry.casefold():
                entrylist.append(entry)

        return render(
            request,
            "encyclopedia/search.html",
            {
                "entries": util.list_entries(),
                "entrylist": entrylist,
                "query": query,
                "message": f"'{query}' does not match any entry.",
            },
        )

    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


# Returns entry and content of given title
def entry(request, title):
    if util.get_entry(title) is None:
        return render(
            request,
            "encyclopedia/error.html",
            {"message": f"The entry '{title}' does not exist in the encyclopdia."},
        )
    return render(
        request,
        "encyclopedia/entry.html",
        {"entry": markdown(util.get_entry(title)), "title": title},
    )


# Returns random encyclopedia entry
def random(request):
    # n.B. Could not get 'choice()' to import; worked in terminal though
    list = util.list_entries()
    length = len(list)
    random_num = randint(0, length - 1)
    return render(
        request,
        "encyclopedia/entry.html",
        {
            "entry": markdown(util.get_entry(list[random_num])),
            "title": list[random_num],
        }
    )


# Adds page for new entry through form POST
def add(request):
    entries = util.list_entries()
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            title = form.cleaned_data["title"]
            if title in entries:
                return render(
                    request,
                    "encyclopedia/error.html",
                    {"message": f"The entry '{title}' already exists."},
                )
            else:
                util.save_entry(title, entry)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/add.html", {"form": form})

    return render(request, "encyclopedia/add.html", {"form": NewEntryForm()})


# Present entry content for editing with Markdown
def edit(request):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["entry"]
            title = form.cleaned_data["title"]
            util.save_entry(title, content)
            return render(
                request,
                "encyclopedia/entry.html",
                {"entry": markdown(util.get_entry(title)), "title": title}
            )

        else:
            message = "Invalid form submission."
            return render(request, "encyclopedia/edit.html", {"message": message})

    title = request.GET["title"]
    return render(
        request,
        "encyclopedia/edit.html",
        {
            "form": EditEntryForm(
                initial={"entry": util.get_entry(title), "title": title}
            ), "title": title
        }
    )
