from .models import Item
from .models import List
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
    def test_uses_home_page_template(self):

        response = self.client.get('/lists/')

        self.assertTemplateUsed(response, 'lists/home_page.html')
        self.assertContains(response, '<title>To-Do lists</title>')

    def test_only_save_items_when_necessary(self):
        self.client.get('/lists/')
        self.assertEqual(Item.objects.count(), 0)


# 测试 ItemModel
class ListAndItemModelTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_saving_and_retrieving_list_and_items(self):
        list_ = List.objects.create()

        item_1 = Item.objects.create(todo_list=list_, text='item1')
        item_2 = Item.objects.create(todo_list=list_, text='item2')
        item_3 = Item.objects.create(todo_list=list_, text='item3')

        saved_items = Item.objects.all()
        saved_list = List.objects.first()

        self.assertEqual(saved_items.count(), 3)
        self.assertEqual(saved_list.item_set.count(), 3)

        self.assertIn(item_1.text, [item.text for item in saved_items])
        self.assertIn(item_2.text, [item.text for item in saved_items])
        self.assertIn(item_3.text, [item.text for item in saved_items])

        saved_item1 = Item.objects.get(pk=1)
        saved_item2 = Item.objects.get(pk=2)
        self.assertEqual(item_1.text, saved_item1.text)
        self.assertEqual(saved_item1.todo_list, saved_item2.todo_list)


class ListViewTest(TestCase):
    def test_uses_correct_template(self):
        response = self.client.get('/lists/only_one_list_in_the_world/')
        self.assertTemplateUsed(response, 'lists/view_list.html')

    def test_displays_all_items(self):
        todo_list = List.objects.create()
        item1 = Item.objects.create(text="todo1", todo_list=todo_list)
        item2 = Item.objects.create(text="todo2", todo_list=todo_list)

        response = self.client.get('/lists/only_one_list_in_the_world/')

        self.assertContains(response, item1.text)
        self.assertContains(response, item2.text)

    def test_can_save_a_POST_request(self):
        # 发送一个 post请求被那个携带数据
        data = dict(
            item_text='todo1',
        )

        self.client.post('/lists/new', data=data)

        # 这里的 post 操作可以认为将发送请求到处理请求(包括页面跳转)一个原子操作。
        self.assertEqual(Item.objects.count(), 1)
        saved_item = Item.objects.first()
        self.assertEqual(saved_item.text, data['item_text'])

    def test_redirect_after_POST(self):
        data = dict(
            item_text='todo1',
        )
        response = self.client.post('/lists/new', data=data)
        self.assertRedirects(response, '/lists/only_one_list_in_the_world/')
