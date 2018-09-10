from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

LISTS_URL = 'http://localhost:8000/lists/'
MAX_SECONDS = 5


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Safari()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get(LISTS_URL)
        self.assertIn('To-Do', self.browser.title)

    def test_store_lists_and_can_retrieve_it_later(self):
        # 验证文本中的h1 标签的内容
        self.browser.get(LISTS_URL)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'),
                         'Enter a to-do item'
                         )

        todo1 = '##test1'
        input_box.send_keys(todo1)
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        content = self.browser.find_element_by_id('id_list_table').text
        self.assertIn(f'1:{todo1}', content)


if __name__ == '__main__':
    unittest.main()
