from flask import Flask, json
from infra.db import DBManager
from domain.movies import MoviesManager

DB_URL = './data/movies.db'
DATAFILE_URL = './data/movieslist.csv'

db_manager = DBManager(DB_URL)

def create_app():
    app = Flask(__name__)

    db_manager.init_db(DATAFILE_URL)

    return app

app = create_app()

@app.route('/')
def index():
    result = 'Hello Movies!'
    
    return json.jsonify(result)

@app.route('/movies/worst_winners')
def get_worst_winners():
    movies_manager = MoviesManager()
    result = movies_manager.get_worst_winners(db_manager)
    
    return json.jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)