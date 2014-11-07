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
        inputbox.send_keys("Buy Milk")

        # When hit enter, the page updates, and now the page lists
        # "1: Buy Milk"
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy Milk')

        # There is still a text box invinting the user to add another item.
        # the user enters "Drink Milk"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("Drink Milk")
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on the list
        self.check_for_row_in_list_table('1: Buy Milk')
        self.check_for_row_in_list_table('2: Drink Milk')

        # User see unique generated URL -- with some explanatory text
        self.fail('Finish the test!')

        # User visit the URL - the to-do list is still there.

        # user closes everything.


if __name__ == '__main__':
    # warnings='ignore' is used to avoid some traceback errors, with Django 1.7.1
    unittest.main(warnings='ignore')
