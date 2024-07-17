from flask import Flask, json
from db import DBManager
from movies import MoviesManager

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

# @app.route('/')
# def index():
#     return render_template(template_name_or_list='index.html', todos=todos)

# @app.route('/create', methods=['POST'])
# def create():
#     todo = request.form
#     todos.append(todo)

#     return redirect(url_for('index'))

# @app.route('/delete/<int:id>', methods=['DELETE'])
# def delete():
#     del todos

#     return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)