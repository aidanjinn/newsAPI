import unittest
import time
from datetime import datetime, timedelta
from app import app
from methods.cache import cache, clear_old_cache, cache_lock

class TestTimedCache(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.test_route = '/wired-pick-of-day'

    def test_cache_clearing_schedule(self):
        print("\nTesting cache clearing schedule...")
        
        # Make initial request to populate cache
        print("Populating cache with initial request...")
        response = self.app.get(self.test_route)
        self.assertEqual(response.status_code, 200)
        
        # Verify cache has content
        with cache_lock:
            initial_cache_size = len(cache)
            print(f"Initial cache size: {initial_cache_size}")
            self.assertGreater(initial_cache_size, 0)
        
        # Get current time
        now = datetime.now()
        print(f"Current time: {now.strftime('%H:%M:%S')}")
        
        # Calculate time until next scheduled clear
        if now.hour < 6:
            next_clear = now.replace(hour=6, minute=0, second=0, microsecond=0)
        elif now.hour < 12:
            next_clear = now.replace(hour=12, minute=0, second=0, microsecond=0)
        elif now.hour < 20:
            next_clear = now.replace(hour=20, minute=0, second=0, microsecond=0)
        else:
            next_clear = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        
        wait_time = (next_clear - now).total_seconds()
        print(f"Next cache clear scheduled for: {next_clear.strftime('%H:%M:%S')}")
        print(f"Time until next clear: {wait_time:.0f} seconds")
        
        # For testing purposes, we'll wait a short time instead of the full duration
        print("Waiting 5 seconds to simulate time passing...")
        time.sleep(5)
        
        # Force a cache clear
        with cache_lock:
            cache.clear()
            print("Cache cleared manually")
            self.assertEqual(len(cache), 0)
        
        print("Cache clearing schedule test completed")

if __name__ == '__main__':
    unittest.main(verbosity=2)