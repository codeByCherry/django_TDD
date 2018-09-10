from .models import Item

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse


# Create your views here.
def home_page(request):
    if request.method == "POST":
        item_text = request.POST['item_text']
        context = dict(
            new_item_text=item_text,
        )
        item = Item(text=item_text)
        item.save()
        return redirect(reverse('lists:home_page'))
    else:
        items = Item.objects.all()
        context = dict(
            items=items,
        )
        return render(request, 'lists/home_page.html', context=context)
