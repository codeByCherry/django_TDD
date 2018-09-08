from django.shortcuts import render


# Create your views here.
def home_page(request):
    context = dict()
    return render(request, 'lists/home_page.html', context=context)
