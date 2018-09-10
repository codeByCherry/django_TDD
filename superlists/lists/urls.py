from django.urls import path
from .views import home_page
from .views import view_list


app_name = 'lists'

urlpatterns = [
    path('', home_page, name='home_page'),
    path('only_one_list_in_the_world/', view_list, name='view_list'),
]