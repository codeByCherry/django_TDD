from .models import Item

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse


# Create your views here.
def home_page(request):
    if request.method == "POST":
        item_text = request.POST['item_text']
        Item.objects.create(text=item_text)
        #return redirect('/lists/')
        return redirect('/lists/only_one_list_in_the_world')
    else:
        items = Item.objects.all()
        context = dict(
            items=items,
        )
        return render(request, 'lists/home_page.html', context=context)
