from django.test import TestCase
from django.urls import resolve
from .views import home_page
from django.http import HttpRequest


# Create your tests here.
class HomePageTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # 确认当前'/' 对应的views 函数是 home_page
    def test_root_url_resolve_to_home_page_view(self):
        response = self.client.get('/lists/')
        response_content = response.content.decode()

        self.assertTemplateUsed(response, 'lists/home_page.html')
        self.assertIn('<title>To-Do lists</title>', response_content)

    def test_can_save_a_POST_request(self):
        # 发送一个 post请求被那个携带数据
        data = dict(
            item_text='todo1',
        )

        # 这里的 post 操作可以认为将发送请求到处理请求(包括页面跳转)一个原子操作。
        response = self.client.post('/lists/', data=data)

        self.assertIn(data['item_text'], response.content.decode())
