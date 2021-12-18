# from datetime import time
from selenium import webdriver
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.options import Options
from django.urls import reverse
from tests.conf_tests import selecionar_app
import time, sys, os
from threading import local
from django.conf import settings
from django.contrib.auth import (
    SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY,
    get_user_model
)
from django.contrib.sessions.backends.db import SessionStore


tests_local = local()

def create_session_cookie(username, password):
    # First, create a new test user
    user = get_user_model()
    user.objects.create_user(username=username, password=password)

    # Then create the authenticated session using the new user credentials
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()

    # Finally, create the cookie dictionary
    cookie = {
        'name': settings.SESSION_COOKIE_NAME,
        'value': session.session_key,
        'secure': False,
        'path': '/',
    }
    return cookie

class TestProjectIndex(StaticLiveServerTestCase):
    # def test_foo(self):
    #     self.assertEquals(0, 1)
    def setUp(self):
        # print('PATHHHHHHHHHHHHHHHH')
        # print(os.path.join(settings.BASE_DIR, 'tests\\functional_tests\\chromedriver.exe'))
        # options = webdriver.ChromeOptions()
        # options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        # chrome_driver_binary = os.path.join(settings.BASE_DIR, 'tests\\functional_tests\\chromedriver.exe')
        # driver = webdriver.Chrome('functional_tests/chromedriver.exe')
        # options = webdriver.ChromeOptions()
        # options.binary_location = os.path.join(settings.BASE_DIR, 'tests\\functional_tests\\chromedriver.exe')
        # chrome_driver_binary = os.path.join(settings.BASE_DIR, 'tests\\functional_tests\\chromedriver.exe')
        # # self.browser = webdriver.Chrome()
        # driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
        # options = Options()
        # options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
        # driver = webdriver.Chrome(chrome_options=options, executable_path=os.path.join(settings.BASE_DIR, 'tests\\functional_tests\\chromedriver.exe'), )
        # driver.get('http://google.com/')
        # self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
        options = Options()
        options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        self.browser = webdriver.Chrome(chrome_options=options, executable_path=os.path.join(settings.BASE_DIR, 'tests\\functional_tests\\chromedriver.exe'))
        
        
    
    def tearDown(self):
        self.browser.close()
    
    
    @selecionar_app(app='gere_coworking')
    def test_index(self):
        self.browser.get(self.live_server_url)
        # navbar = self.browser.find_element_by_class_name("align-items-center")
        # nav_children = navbar.find_elements_by_css_selector("*")
        # div = nav_children[0]
        # div_children = div.find_elements_by_css_selector("*")
        # h1 = div_children[0]
        h1 = self.browser.find_element_by_tag_name('h1')
        a = h1.find_elements_by_css_selector("*")[0]
        
        self.assertEquals(
            a.text, 'MILLENIA'
        )
        
        logo = self.browser.find_element_by_class_name("img-fluid")
        
        self.assertEquals(
            'media/client_logo/Screenshot_262.png' in logo.get_attribute("src"),
            True
        )
    
    def test_login(self):
        # self.browser.get(self.live_server_url + 'accounts/loginSystem')
        # self.browser.find_element_by_class_name("img-fluid")
        # c = Client()
        # logged_in = c.login(username='testuser', password='12345')
        # id_username
        # self.browser.find_element_by_link_text("MILLENIA")
         #Native django test client
        
        self.client.login(username='42768138835', password='newgen123')
        self.browser.get(self.live_server_url)  #selenium will set cookie domain based on current page domain
        self.browser.add_cookie({'name': 'sessionid', 'value': create_session_cookie('42768138835', 'newgen123').value, 'secure': False, 'path': '/'})
        self.browser.refresh() #need to update page for logged in user
        self.browser.get(self.live_server_url)
        
    # def test_index_check_logo(self):
    #     self.browser.get(self.live_server_url)
    #     logo = self.browser.find_element_by_class_name("img-fluid")
        
    #     self.assertEquals(
    #         'media/client_logo/Screenshot_262.png' in logo.get_attribute("src"),
    #         True
    #     )