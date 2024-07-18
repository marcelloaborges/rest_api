import unittest
from app import app
import json

class FlaskIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_movies_worst_winners(self):
        response = self.client.get("/movies/worst_winners")

        self.assertEqual(response.status_code, second=200)
        self.assertEqual(response.content_type, second='application/json')
        
        if not "min" in response.json:
            raise ValueError("Missing key 'min' in result")
        
        if not "max" in response.json:
            raise ValueError("Missing key 'max'  in result")
        
        self.assertGreater(len(response.json["min"]), 0)
        self.assertGreater(len(response.json["max"]), 0)

        if not "producer" in response.json["min"][0]:
            raise ValueError("Missing key 'producer' in result/min")
        if not "interval" in response.json["min"][0]:
            raise ValueError("Missing key 'interval' in result/min")
        if not "previousWin" in response.json["min"][0]:
            raise ValueError("Missing key 'previousWin' in result/min")
        if not "followingWin" in response.json["min"][0]:
            raise ValueError("Missing key 'followingWin' in result/min")

        if not "producer" in response.json["max"][0]:
            raise ValueError("Missing key 'producer' in result/max")
        if not "interval" in response.json["max"][0]:
            raise ValueError("Missing key 'interval' in result/max")
        if not "previousWin" in response.json["max"][0]:
            raise ValueError("Missing key 'previousWin' in result/max")
        if not "followingWin" in response.json["max"][0]:
            raise ValueError("Missing key 'followingWin' in result/max")

        if len(response.json["min"]) > 0:
            previous_interval_value = 1000
            for min_winners in response.json["min"]:
                if previous_interval_value == 1000:
                    previous_interval_value = min_winners["interval"]
                    continue
                if previous_interval_value != min_winners["interval"]:
                    raise ValueError("Winner min movies must have the same interval")
                
        if len(response.json["max"]) > 0:
            previous_interval_value = -1
            for min_winners in response.json["max"]:
                if previous_interval_value == -1:
                    previous_interval_value = min_winners["interval"]
                    continue
                if previous_interval_value != min_winners["interval"]:
                    raise ValueError("Winner max movies must have the same interval")
