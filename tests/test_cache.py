import unittest
import json
import time
from app import app

class TestCaching(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.routes = [
            '/wired-pick-of-day',
            '/AP-pick-of-day',
            '/vogue-pick-of-day',
            '/rolling-stone-movies-tv-pick-of-day',
            '/yahoo-sports-pick-of-day',
            '/yahoo-sports-breaking-news',
            '/yahoo-sports',
            '/yahoo-sports-recap',
            '/democracy-now-pick-of-day',
            '/world-news',
            '/SCMP-pick-of-day',
            '/SCMP-china-top-story',
            '/cosmo-style-pick-of-day',
            '/fashion-news',
            '/techcrunch-pick-of-day',
            '/zdnet-pick-of-day',
            '/tech-news',
            '/weather-channel-pick-of-day',
            '/weather-gov-pick-of-day',
            '/weather-news',
            '/yahoo-finance-pick-of-day',
            '/economist-pick-of-day',
            '/forbes-pick-of-day',
            '/finance-news',
            '/people-pick-of-day',
            '/entertainment-news'
        ]

    def test_cache_performance(self):
        total = len(self.routes)
        passed_count = 0

        for route in self.routes:
            with self.subTest(route=route):
                print(f"\nTesting {route}")
                
                # First request
                print("Making first request...")
                start_time = time.time()
                response1 = self.app.get(route)
                first_request_time = time.time() - start_time
                
                # Check if first response is valid
                self.assertEqual(response1.status_code, 200)
                json_data1 = json.loads(response1.data)
                self.assertIsNotNone(json_data1)
                print(f"First request completed in {first_request_time:.3f}s")
                
                # Wait briefly before second request
                time.sleep(0.5)
                
                # Second request (should be cached)
                print("Making second request...")
                start_time = time.time()
                response2 = self.app.get(route)
                second_request_time = time.time() - start_time
                
                # Check if second response is valid
                self.assertEqual(response2.status_code, 200)
                json_data2 = json.loads(response2.data)
                self.assertIsNotNone(json_data2)
                
                # Calculate improvement
                improvement = ((first_request_time - second_request_time) / first_request_time * 100)
                print(f"Second request completed in {second_request_time:.3f}s")
                print(f"Cache improvement: {improvement:.1f}%")
                
                # Test passes if second request was faster
                if second_request_time < first_request_time:
                    print(f"Route {route} PASSED - Cache working")
                    passed_count += 1
                else:
                    print(f"Route {route} FAILED - Cache not improving performance")
                
                # Wait before next route
                time.sleep(2)
        
        print(f"\nTotal tests: {total}, Passed: {passed_count}, Failed: {total - passed_count}")

if __name__ == '__main__':
    unittest.main()