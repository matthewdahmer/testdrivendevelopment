from selenium import webdriver
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
        # Open the to-do app home page
        self.browser.get('http://localhost:8000')

        # The page title and header should mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')


        # This is what we want to see:
        #
        # The option to insert an item to the list right away.
        #
        # Enter the list item into a text box and hit enter/return.
        #
        # When hitting enter/return, the page updates and lists the first item.
        #
        # There is still a text box to enter additional list items.
        #
        # One item can be entered at a time.
        #
        # Each time an item is entered and the enter/return key is pressed, the list updates.
        #
        # The site generates a unique url for each user, where the list is stored. This feature is
        # described on the page where the initial list is generated.
        #
        # Visiting this unique url will show the list is indeed stored at that location.

if __name__ == '__main__':
    unittest.main(warnings='ignore')

