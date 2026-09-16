from django.shortcuts import render


from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, "test_app/index.html", {
        "title": "Home",
        "content": "This is the home page."
    })
