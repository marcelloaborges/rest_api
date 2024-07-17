from infra.db import DBManager

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

        studios_with_more_than_one_prize = self._get_studios_with_more_than_one_prize(worst_movies)
        
        faster_studios = self._get_faster_studios_prizes(studios_with_more_than_one_prize)
        slower_studios = self._get_slower_studios_prizes(studios_with_more_than_one_prize)

        result = {
            "min": [],
            "max": []
        }

        for studio in faster_studios:
            result["min"].append(studio)

        for studio in slower_studios:
            result["max"].append(studio)

        return result
        
    def _get_studios_with_more_than_one_prize(self, movies):
        studios_movies = {}

        for movie in movies:
            # year;title;studios;producers;winner
            studio = movie[self.STUDIOS]
            if studio not in studios_movies:
                studios_movies[studio] = [movie]                
            else:
                studios_movies[studio].append(movie)

        studios_with_more_than_one_prize = {}
        for studio, movies in studios_movies.items():
            if len(movies) == 1:
                continue

            studios_with_more_than_one_prize[studio] = movies        

        return studios_with_more_than_one_prize
    
    def _get_faster_studios_prizes(self, studios_movies):
        studios_min_prize_interval = {}
        for studio, movies in studios_movies.items():
            
            studios_min_prize_interval[studio] = {                
                "interval": 10000,
                "previousWin": 0,
                "followingWin": 0
            }
            i = 0
            for j in range(1, len(movies)):
                diff = movies[j][self.YEAR] - movies[i][self.YEAR]
                if diff < studios_min_prize_interval[studio]["interval"]:                    
                    studios_min_prize_interval[studio]["interval"] = diff
                    studios_min_prize_interval[studio]["previousWin"] = movies[i][self.YEAR]
                    studios_min_prize_interval[studio]["followingWin"] = movies[j][self.YEAR]
                i = j

        studios_min_prize_interval = {k: v for k, v in sorted(studios_min_prize_interval.items(), key=lambda item: item[1]["interval"])}

        faster_studios = []
        for studio, interval in studios_min_prize_interval.items():
            if faster_studios:
                if interval["interval"] > faster_studios[-1]["interval"]:
                    break

            faster_studios.append(
                {
                    "producer": studio,
                    "interval": interval["interval"],
                    "previousWin": interval["previousWin"],
                    "followingWin": interval["followingWin"]
                }
            )

        return faster_studios
    
    def _get_slower_studios_prizes(self, studios_movies):
        studios_max_prize_interval = {}
        for studio, movies in studios_movies.items():
            
            studios_max_prize_interval[studio] = {                
                "interval": -1,
                "previousWin": 0,
                "followingWin": 0
            }
            i = 0
            for j in range(1, len(movies)):
                diff = movies[j][self.YEAR] - movies[i][self.YEAR]
                if diff > studios_max_prize_interval[studio]["interval"]:                    
                    studios_max_prize_interval[studio]["interval"] = diff
                    studios_max_prize_interval[studio]["previousWin"] = movies[i][self.YEAR]
                    studios_max_prize_interval[studio]["followingWin"] = movies[j][self.YEAR]
                i = j

        studios_max_prize_interval = {k: v for k, v in sorted(studios_max_prize_interval.items(), key=lambda item: item[1]["interval"], reverse=True)}

        faster_studios = []
        for studio, interval in studios_max_prize_interval.items():
            if faster_studios:
                if interval["interval"] < faster_studios[-1]["interval"]:
                    break

            faster_studios.append(
                {
                    "producer": studio,
                    "interval": interval["interval"],
                    "previousWin": interval["previousWin"],
                    "followingWin": interval["followingWin"]
                }
            )

        return faster_studios

