from .models import Item
from .models import List

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse


# Create your views here.
def home_page(request):
    return render(request, 'lists/home_page.html')


def view_list(request):
    if request.method == "POST":
        item_text = request.POST['item_text']
        Item.objects.create(text=item_text)
        return redirect(reverse('lists:view_list'))

    items = Item.objects.all()
    context = dict(
        items = items,
    )
    return render(request, 'lists/view_list.html', context)


def add_item(request):
    item_text = request.POST['item_text']
    todo_list = List.objects.create()
    Item.objects.create(text=item_text, todo_list=todo_list)
    return redirect(reverse('lists:view_list'))
