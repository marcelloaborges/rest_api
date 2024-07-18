import unittest
from app import app, db_manager
from infra.db import DBManager

DB_URL = './data/movies.db'
DATAFILE_URL = './data/movieslist.csv'

class FlaskIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()        

    def test_movies_worst_winners_not_found(self):
        db_manager = DBManager(DB_URL)        
        db_manager._create_table_movies()

        response = self.client.get("/movies/worst_winners")

        self.assertEqual(response.status_code, second=404)
        self.assertEqual(response.content_type, second='text/html; charset=utf-8')
        self.assertEqual(response.text, second='Data not found')        

    def test_movies_worst_winners(self):
        db_manager = DBManager(DB_URL)
        db_manager.init_db(DATAFILE_URL)

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

    def test_db_create_successfully_with_movies(self):
        sql_command = """
            SELECT * FROM movies
        """
        
        result = db_manager.execute_query(sql_command)

        self.assertGreater(len(result), 0)
        
