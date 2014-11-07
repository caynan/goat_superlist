from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = self.browser.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User enters To-Do homepage
        self.browser.get(self.live_server_url)

        # The page title and header mention To-Do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # The user is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # The user types "Buy Milk" into a text box
        inputbox.send_keys("Buy peacock feathers")

        # When hit enter, the page updates, and now the page lists
        # "1: Buy Milk"
        inputbox.send_keys(Keys.ENTER)
        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box invinting the user to add another item.
        # the user enters "Drink Milk"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on the list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # A new user, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of the first user is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # New user visits the home page. There is no sign of the first user
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Use peacock feathers to make a fly', page_text)

        # New user starts a new list.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # New user gets it's own unique URL
        newuser_list_url = self.browser.current_url
        self.assertRegex(newuser_list_url, '/lists/.+')
        self.assertNotEqual(newuser_list_url, user_list_url)

        # Again, there is no trace of first user's list
        page_text = self.browser.find_element_by_tag('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Happy, the user closes everything sure that they'll be there tomorrow.


if __name__ == '__main__':
    # warnings='ignore' is used to avoid some traceback errors, with Django 1.7.1
    unittest.main(warnings='ignore')
