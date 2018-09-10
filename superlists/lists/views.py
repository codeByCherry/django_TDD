from .models import Item

from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home_page(request):
    if request.method == "POST":
        item_text = request.POST['item_text']
        context = dict(
            new_item_text=item_text,
        )
        item = Item(text=item_text)
        item.save()
    else:
        context = dict()
    return render(request, 'lists/home_page.html', context=context)
