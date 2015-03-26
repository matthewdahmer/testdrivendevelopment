from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        ## A 1-3 second delay is necessary to give firefox a chance to load to avoid the error:
        ##
        ## selenium.common.exceptions.WebDriverException: Message: The browser appears to have
        ## exited before we could connect...
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Zac wants to check out this new to-do list online
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists, this is good because otherwise
        # he might be a bit dissapointed and confused (he can read)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Zac is only 5, and not particularly good at finding things sometimes, so it's good that
        # he sees a text box in the home page (not eslewhere) where he can start his to do list
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # Zac types "clean up my room" into the text box (he needs to do this more often)
        inputbox.send_keys('clean up my room')

        # When he hits enter/return, he is taken to a new URL, and now the page lists
        # "1: clean up my room" as an item in the to-do list table
        inputbox.send_keys(Keys.ENTER)
        zac_list_url = self.browser.current_url
        self.assertRegex(zac_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: clean up my room')

        # There is still a text box to enter additional list items, which is good because there
        # are many other things Zac needs to do. He enters 'learn to tie my shoes'.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('learn to tie my shoes')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and shows both items on his list
        self.check_for_row_in_list_table('1: clean up my room')
        self.check_for_row_in_list_table('2: learn to tie my shoes')

        # Now a new user, Ethan, comes along to the site

        ## We use a new browser session to make sure that no information of Zac's is coming
        ## through from cookies, etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Ethan visits the home page. There is no sign of Zac's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: clean up my room', page_text)
        self.assertNotIn('2: learn to tie my shoes', page_text)

        # Ethan starts a new list by entering a new item. He is less focused on being responsible
        # than Zac and just wants to play.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Play Minecraft')
        inputbox.send_keys(Keys.ENTER)

        # Ethan gers his own unique URL
        ethan_list_url = self.browser.current_url
        self.assertRegex(ethan_list_url, '/lists/.+')
        self.assertNotEqual(zac_list_url, ethan_list_url)

        # Again, there is no trace of Zac's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('clean up my room', page_text)
        self.assertIn('Play Minecraft', page_text)

        # Satisfied, they both go back to sleep, or not...

        self.fail('Finish the test!')

        #
        # Each time an item is entered and the enter/return key is pressed, the list updates.
        #
        # The site generates a unique url for each user, where the list is stored. This feature is
        # described on the page where the initial list is generated.
        #
        # Visiting this unique url will show the list is indeed stored at that location.
