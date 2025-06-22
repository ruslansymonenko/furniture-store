from django.shortcuts import render

def index(request):
    context = {
        'title': 'Store: Home Page',
        'content': 'Furniture Store',
    }

    return render(request, 'main/home.html', context)

def about(request):
    context = {
        'title': 'Store: About Page',
        'content': 'About us',
        'text_on_page': 'This is furniture store with best products'
    }

    return render(request, 'main/about.html', context)