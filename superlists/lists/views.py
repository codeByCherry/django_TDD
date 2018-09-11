from .models import Item
from .models import List

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse


# Create your views here.
def home_page(request):
    return render(request, 'lists/home_page.html')


def view_list(request, list_id):
    todo_list = get_object_or_404(List, pk=list_id)
    items = todo_list.item_set.all()
    context = dict(
        items=items,
        todo_list=todo_list,
    )
    return render(request, 'lists/view_list.html', context)


def new_list(request):
    todo_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], todo_list=todo_list)
    return redirect(reverse('lists:view_list', args=(todo_list.id, )))


def add_item(request, list_id):
    todo_list = get_object_or_404(List, pk=list_id)
    item_text = request.POST['item_text']
    Item.objects.create(text=item_text, todo_list=todo_list)
    #return redirect(f'/lists/{list_id}/')
    return redirect(reverse('lists:view_list', args=(list_id,)))
