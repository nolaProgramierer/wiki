from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from . import util
from random import randint


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    entry = forms.CharField(
        label="Create Entry", widget=forms.Textarea(attrs={"size": 3, "cols": 10})
    )


# GET request in form returns query result
# or the GET request returns list of all encyclopedia entries
def index(request):
    query = request.GET.get("q")
    if util.get_entry(query):
        return render(
            request, "encyclopedia/entry.html", {"entries": util.get_entry(query)}
        )
    # Check GET query in encycclopedia search entries
    elif util.get_entry(query) is not query:
        entrylist = []
        for entry in util.list_entries():
            if query in entry:
                entrylist.append(entry)
        context = {
            "entries": util.list_entries(),
            "entrylist": entrylist,
            "query": query,
            "message": f"'{query}' does not match any entry.",
        }
        return render(request, "encyclopedia/search.html", context)

    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


# Returns emtry and definition of title
def entry(request, title):
    if util.get_entry(title) is None:
        return render(
            request,
            "encyclopedia/error.html",
            {"message": f"The entry '{title}' does not exist in the encyclopdia"},
        )
    return render(
        request, "encyclopedia/entry.html", {"entries": util.get_entry(title)}
    )


# Returns random encyclopedia entry
def random(request):
    list = util.list_entries()
    length = len(list)
    random_num = randint(0, length - 1)
    return render(
        request,
        "encyclopedia/entry.html",
        {"entries": util.get_entry(list[random_num])},
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

