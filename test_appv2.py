import pytest
from flask_testing import TestCase
from appv2 import app

class MyTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        return app

        # Just a test to ensure that redirect functions.
    def test_home_redirect(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/current-season')

        # Ensures the expected template is used in response
    def test_current_season_anime(self):
        response = self.client.get('/current-season')
        self.assertEqual(response.status_code, 200)
        self.assertIn('anime_list.html', response.data.decode('utf-8'))  

    def test_rate_limiter(self):
        # First request should pass
        response1 = self.client.get('/current-season')
        self.assertEqual(response1.status_code, 200)

        # Immediate second request should fail due to rate limiting
        response2 = self.client.get('/current-season')
        self.assertEqual(response2.status_code, 429)
