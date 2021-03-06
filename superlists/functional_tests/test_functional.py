from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import os
#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

MAX_SECONDS = 5

WINDOW_HEIGHT = 768
WINDOW_WIDTH = 1333


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Safari()

        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        else:
            print(f'\nYou can set ip address like "192.168.1.1" to STAGING_SERVER')

    def tearDown(self):
        self.browser.quit()

    def check_input_box_center(self, input_box):
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width']*0.5,
            WINDOW_WIDTH*0.5,
            delta=100,
        )

    def check_for_row_in_list_table(self, row_text, index=1):
        start_time = time.time()
        while True:
            try:
                table_text = self.browser.find_element_by_id('id_list_table').text
                self.assertIn(f'{index}:{row_text}', table_text)
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time >= MAX_SECONDS:
                    raise e
                time.sleep(0.2)

    def test_title(self):
        self.browser.get(self.live_server_url+'/lists/')
        self.assertIn('To-Do', self.browser.title)

    def test_can_start_a_list_for_one_user(self):
        # 验证文本中的h1 标签的内容
        self.browser.get(self.live_server_url+'/lists/')
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'),
                         'Enter a to-do item'
                         )

        todo1 = '##test1'
        input_box.send_keys(todo1)
        input_box.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table(todo1,1)

        todo2 = '##test2'
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(todo2)
        input_box.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table(todo1, 1)
        self.check_for_row_in_list_table(todo2, 2)

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url+'/lists/')
        input_box = self.browser.find_element_by_id('id_new_item')
        user1_item = '#user1 todo item'
        input_box.send_keys(user1_item)
        input_box.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table(user1_item, 1)

        user1_list_url = self.browser.current_url
        self.assertRegex(user1_list_url, '/lists/.+')

        ## 这里为了避免缓存的 session 的影响，手动关闭该 browser
        ## 确保一个干净的新 session
        self.browser.quit()
        self.browser = webdriver.Safari()
        self.browser.get(self.live_server_url+'/lists/')

        user2_item1 = '#user2 item1'
        user2_item2 = '#user2 item2'

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(user2_item1)
        input_box.send_keys(Keys.ENTER)

        time.sleep(0.2)
        self.assertNotIn(
            user1_item,
            self.browser.find_element_by_id('id_list_table').text,
        )
        self.check_for_row_in_list_table(user2_item1, 1)

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys(user2_item2)
        input_box.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table(user2_item1, 1)
        self.check_for_row_in_list_table(user2_item2, 2)

        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user1_list_url, user2_list_url)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url+'/lists/')
        self.browser.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        input_box = self.browser.find_element_by_id('id_new_item')

        self.check_input_box_center(input_box)

        input_box.send_keys('todo1')
        input_box.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('todo1')
        self.browser.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        input_box = self.browser.find_element_by_id('id_new_item')
        self.check_input_box_center(input_box)



