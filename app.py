from flask import Flask, render_template, request, url_for, send_from_directory, redirect
import db

DB_URL = './data/movies.db'
DATAFILE_URL = './data/movieslist.csv'

def create_app():
    app = Flask(__name__)

    with app.app_context():
        db.init_db(DB_URL, DATAFILE_URL)

    return app


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
    app = create_app()

    app.run(debug=True)