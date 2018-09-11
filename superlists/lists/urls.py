from django.urls import path
from .views import home_page
from .views import view_list
from .views import new_list
# from .views import add_item


app_name = 'lists'

urlpatterns = [
    path('', home_page, name='home_page'),
    path('<int:list_id>/', view_list, name='view_list'),
    path('new', new_list, name='new_list'),
]