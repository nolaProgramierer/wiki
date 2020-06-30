from django.shortcuts import render

from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"The entry '{title}' does not exist in the encyclopdia"
        })
    return render (request, "encyclopedia/entry.html", {
        "entries": util.get_entry(title)
    })