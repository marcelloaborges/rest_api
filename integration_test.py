from flask_testing import TestCase
from app import app
import json

# class FlaskIntegrationTestCase(TestCase):

    # def set_up(self):
    #     app.config["TESTING"] = True
    #     self.client = app.test_client()

class BaseTestCase(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        return app

class MoviesTest(BaseTestCase):
    def test_movies_worst_winners(self):
        response = self.client.get('/movies/worst_movies')
        
        self.assertEqual(response.status_code, second=200)
        
        data = json.loads(response.content)
        assert data["status"] == "0"
        
        if not "min" in response:
            raise ValueError("Missing key 'min' in result")
        
        if not "max" in response:
            raise ValueError("Missing key 'max'  in result")