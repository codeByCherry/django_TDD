from django.test import TestCase
from django.urls import resolve
from .views import home_page
from django.http import HttpRequest

# Create your tests here.
class HomePageTest(TestCase):

    def setUp(self):
        pass

    # 确认当前'/' 对应的views 函数是 home_page
    def test_root_url_resolve_to_home_page_view(self):
        response = self.client.get('/lists/')
        self.assertTemplateUsed(response, 'lists/home_page.html')


