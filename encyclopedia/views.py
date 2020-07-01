from django.shortcuts import render

from django.http import HttpResponse

from . import util

from random import randint

# GET request in form returns query result
# or the GET request returns list of all encyclopedia entries
def index(request):
    query = request.GET.get("q")
    if util.get_entry(query):
        return render(request, "encyclopedia/entry.html", {
            "entries": util.get_entry(query)
        })
    # Check GET query in encycclopedia entries
    elif util.get_entry(query) is not query:
        entrylist = []
        for entry in util.list_entries():
            if query in entry:
                entrylist.append(entry)          
        context = {
            "entries": util.list_entries(),
            "entrylist": entrylist,
            "query": query,
            "message": f"'{query}' does not match any entry."
        }
        return render(request, "encyclopedia/search.html", context)
   
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Returns emtry and definition of title
def entry(request, title):
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"The entry '{title}' does not exist in the encyclopdia"
        })
    return render(request, "encyclopedia/entry.html", {
        "entries": util.get_entry(title)
    })

# Returns random encyclopedia entry
def random(request):
    list = util.list_entries()
    length = len(list)
    random_num = randint(0, length - 1)
    return render(request, "encyclopedia/entry.html", {
            "entries": util.get_entry(list[random_num])
        })