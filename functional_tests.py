from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_ir_later(self):
        self.browser.get('http://localhost:8000')
        # The page title and header mention To-Do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail("finish the test!")

        # The user is invited to enter a to-do item straight away

        # The user types "Buy Milk" into a text box

        # When hit enter, the page updates, and now the page lists
        # "1: Buy Milk"

        # There is still a text box invinting the user to add another item.
        # the user enters "Drink Milk"

        # The page updates again, and now shows both items on the list

        # User see unique generated URL -- with some explanatory text

        # User visit the URL - the to-do list is still there.

        # user closes everything.


if __name__ == '__main__':
    # warnings='ignore' is used to avoid some traceback errors, with Django 1.7.1
    unittest.main(warnings='ignore')
