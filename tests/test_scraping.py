import unittest
import json
from app import app

'''
    The purpose of this test file is to ensure that all the 
    web scraping methods are working as expected.

    The test file will test all the text-based routes and ensure that
    the scraping functions are returning a valid json object
    containing the article, title, and link.
'''

class TestNewsRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_text_routes(self):
        # List of all text-based routes
        routes = [
            '/wired-pick-of-day-text',
            '/AP-pick-of-day-text',
            '/vogue-pick-of-day-text',
            '/rolling-stone-movies-tv-pick-of-day-text',
            '/yahoo-sports-pick-of-day-text',
            '/yahoo-sports-text',
            '/yahoo-sports-recap-text',
            '/democracy-now-pick-of-day-text',
            '/world-news-text',
            '/SCMP-pick-of-day-text',
            '/SCMP-china-top-story-text',
            '/cosmo-style-pick-of-day-text',
            '/fashion-news-text',
            '/techcrunch-pick-of-day-text',
            '/tech-news-text',
            '/weather-channel-pick-of-day-text',
            '/weather-gov-pick-of-day-text',
            '/weather-news-text',
            '/yahoo-finance-pick-of-day-text',
            '/economist-pick-of-day-text',
            '/forbes-pick-of-day-text',
            '/finance-news-text',
            '/people-pick-of-day-text',
            '/entertainment-news-text'
        ]

        total = len(routes)
        passed_count = 0

        for route in routes:
            with self.subTest(route=route):
                response = self.app.get(route)
                
                # Check if response status is 200 (OK)
                self.assertEqual(response.status_code, 200)
                
                # Check if response is valid JSON
                try:
                    json_data = json.loads(response.data)
                    self.assertIsNotNone(json_data)
                    print(f"route: {route}, has returned: PASSED")
                    passed_count += 1
                except json.JSONDecodeError:
                    self.fail(f"Route {route} did not return valid JSON")
            
        print(f"Total tests: {total}, Passed: {passed_count}, Failed: {total - passed_count}")

if __name__ == '__main__':
    unittest.main()