from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # A 1-3 second delay is necessary to give firefox a chance to load to avoid the error:
        #
        # selenium.common.exceptions.WebDriverException: Message: The browser appears to have
        # exited before we could connect...
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Zac wants to check out this new to-do list online
        self.browser.get('http://localhost:8000')

        # He notices the page title and header mention to-do lists, this is good because otherwise
        # he might be a bit dissapointed and confused (he can read)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Zac is only 5, and not particularly good at finding things sometimes, so it's good that
        # he sees a text box in the home page where he can start his to do list
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # Zac types "clean up my room" into the text box (he needs to do this more often)
        inputbox.send_keys('clean up my room')

        # When he hits enter/return, the page updates and now it lists
        # "1: clean up my room" as an item in the to-do list table
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: clean up my room', [row.text for row in rows])

        # There is still a text box to enter additional list items, which is good because there
        # are many other things Zac needs to do. He enters 'learn to tie my shoes'.
        self.assertIn('2: learn to tie my shoes', [row.text for row in rows])

        self.fail('Finish the test!')

        #
        # Each time an item is entered and the enter/return key is pressed, the list updates.
        #
        # The site generates a unique url for each user, where the list is stored. This feature is
        # described on the page where the initial list is generated.
        #
        # Visiting this unique url will show the list is indeed stored at that location.

if __name__ == '__main__':
    unittest.main(warnings='ignore')

