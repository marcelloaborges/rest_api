import csv, sqlite3
import os

class DBManager():

    def __init__(self, db_url:str):
        self._db_url = db_url    

        # CREATE DB FILE
        connection = sqlite3.connect(self._db_url)    
        connection.close()

    def _get_connection(self):
        return sqlite3.connect(self._db_url)

    def execute_query(self, sql_command:str) -> list:
        connection = self._get_connection()
        cursor = connection.cursor()

        result = cursor.execute(sql_command)
        result = result.fetchall()
        connection.close()

        return result

    def execute_command(self, sql_command:str):
        connection = self._get_connection()

        cursor = connection.cursor()
        cursor.execute(sql_command)
        connection.commit()

        connection.close()

    def execute_many(self, sql_command:str, obj_list):
        connection = self._get_connection()

        cursor = connection.cursor()
        cursor.executemany(sql_command, obj_list)
        connection.commit()

        connection.close()

    def init_db(self, datafile_url:str):    

        # DROP THE EXISTING DATABASE IF NECESSARY
        try:
            os.remove(self._db_url)
        except OSError:
            pass

        # DATA SAMPLE
        # year;title;studios;producers;winner
        # 1980;Can't Stop the Music;Associated Film Distribution;Allan Carr;yes                

        # CREATE MOVIES TABLE
        create_table_movies_command = """
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

        self.execute_command(create_table_movies_command)

        # INSERT MOVIES
        with open(datafile_url, 'r') as fin:
            dr = csv.DictReader(fin, delimiter=";")
            obj_list = [(i['year'], i['title'], i['studios'], i['producers'], 1 if i['winner'] == 'yes' else 0) for i in dr]

        insert_movies_command = """
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

        self.execute_many(insert_movies_command, obj_list)        
    