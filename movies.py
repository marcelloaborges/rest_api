from db import DBManager

class MoviesManager():

    def __init__(self) -> None:
        self.ID = 0
        self.YEAR = 1
        self.TITLE = 2
        self.STUDIOS = 3
        self.PRODUCERS = 4
        self.WINNER = 5

        pass

    def get_worst_winners(self, db_manager: DBManager) -> list:
        command = """
            SELECT * FROM MOVIES
            WHERE winner = 1
            ORDER BY year
        """

        worst_movies = db_manager.execute_query(command)        

        studios = {}
        for movie in worst_movies:
            # year;title;studios;producers;winner
            studio = movie[self.STUDIOS]
            if studio not in studios:
                studios[studio] = [movie]                
            else:
                studios[studio].append(movie)

        studios_with_more_than_one_prize = {}
        for studio, movies in studios.items():
            if len(movies) == 1:
                continue

            studios_with_more_than_one_prize[studio] = movies

        faster_studios = {}
        for studio, movies in studios_with_more_than_one_prize.items():
            year_prize1 = 0
            year_prize2 = 0
            for movie in movies:
                year_prize1 = movie[self.YEAR]

        return studios
        
