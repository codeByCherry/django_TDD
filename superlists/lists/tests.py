from .models import Item
from .views import home_page

from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve


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

    # TODO:: 不要把写测试和读测试放在一个单元测试中！记得拆分这个测试
    def test_can_save_a_POST_request(self):
        # 发送一个 post请求被那个携带数据
        data = dict(
            item_text='todo1',
        )

        self.client.post('/lists/', data=data)
        # 这里的 post 操作可以认为将发送请求到处理请求(包括页面跳转)一个原子操作。
        self.assertEqual(Item.objects.count(), 1)

        saved_item = Item.objects.first()
        self.assertEqual(saved_item.text, data['item_text'])

    def test_redirect_after_POST(self):
        data = dict(
            item_text='todo1',
        )
        response = self.client.post('/lists/', data=data)

        self.assertRedirects(response, '/lists/only_one_list_in_the_world')

    def test_only_save_items_when_necessary(self):
        self.client.get('/lists/')
        self.assertEqual(Item.objects.count(), 0)


# 测试 ItemModel
class ItemModelTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_saving_and_retrieving_items(self):
        item_1 = Item()
        item_1.text = 'item1'
        item_1.save()

        item_2 = Item()
        item_2.text = 'item2'
        item_2.save()

        item_3 = Item()
        item_3.text = 'item3'
        item_3.save()

        saved_items = Item.objects.all()

        self.assertEqual(saved_items.count(), 3)
        self.assertIn(item_1.text, [item.text for item in saved_items])
        self.assertIn(item_2.text, [item.text for item in saved_items])
        self.assertIn(item_3.text, [item.text for item in saved_items])

        saved_item1 = Item.objects.get(pk=1)
        self.assertEqual(item_1.text, saved_item1.text)




