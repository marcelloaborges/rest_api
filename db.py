import csv, sqlite3
import os

def init_db(db_url:str, datafile_url:str):
    
    # DROP THE EXISTING DATABASE IF NECESSARY
    try:
        os.remove(db_url)
    except OSError:
        pass

    # DATA SAMPLE
    # year;title;studios;producers;winner
    # 1980;Can't Stop the Music;Associated Film Distribution;Allan Carr;yes

    # CREATE DB FILE
    connection = sqlite3.connect(db_url)
    cursor = connection.cursor()

    # CREATE MOVIES TABLE
    CREATE_TABLE_MOVIES = """
    CREATE TABLE IF NOT EXISTS
    movies(
        id INTEGER PRIMARY KEY, 
        year INTEGER,
        title TEXT,
        studios TEXT,
        producers TEXT,
        winner INTEGER
    )

    """

    cursor.execute(CREATE_TABLE_MOVIES)

    # INSERT MOVIES
    with open(datafile_url, 'r') as fin:
        dr = csv.DictReader(fin, delimiter=";")
        to_db = [(i['year'], i['title'], i['studios'], i['producers'], 1 if i['winner'] == 'yes' else 0) for i in dr]

    INSERT_INTO_MOVIES = """
        INSERT INTO movies
        (
            year,
            title,
            studios,
            producers,
            winner
        )
        VALUES
        (
            ?,
            ?,
            ?,
            ?,
            ?
        )
    """

    # COMMIT AND CLOSE CONNECTION
    cursor.executemany(INSERT_INTO_MOVIES, to_db)
    connection.commit()
    connection.close()