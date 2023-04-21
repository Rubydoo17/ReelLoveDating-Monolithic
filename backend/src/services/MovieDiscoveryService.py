from backend.src.models import Movie, Director, Actor
from imdb import IMDb

from backend.src.repositories import MovieRepository
from backend.src.repositories import DirectorRepository
from backend.src.repositories import ActorRepository


class MovieDiscovery:
    """
    The class that handles the Movie discovery from IMDB and other data sources. It will automatically create
    Movie objects, Actor objects, and Director objects, and store them in the database via their corresponding
    repositories.
    """

    def __init__(self):
        self.apiClient = IMDb()

    def startDiscovery(self):
        """
        Starts the discovery process using the IMDB api to get a list of movies and their corresponding
        actors and directors. It will then create Movie, Actor, and Director objects and store them in the
        database.
        """
        top_movies = self.apiClient.get_top50_movies_by_genres('top_250')
        for movie in top_movies:
            # Getting the movie info from the api.
            title = movie['title']
            year = movie['year']
            # capping the description at 255 characters to fit in the database.
            description = movie['plot'] if len(movie['plot']) < 255 else movie['plot'][::255]
            genre = movie['genres'][0]

            director = movie['directors'][0]
            directorFirstName = director['name'].split(' ')[0]
            directorLastName = director['name'].split(' ')[1]

            leadActor = movie['cast'][0]
            leadActorFirstName = leadActor['name'].split(' ')[0]
            leadActorLastName = leadActor['name'].split(' ')[1]

            print(f"Title: {title}")
            print(f"Year: {year}")
            print(f"Description: {description}")
            print(f"Genre: {genre}")
            print(f"Director Firstname: {directorFirstName}")
            print(f"Director LastName: {directorLastName}")
            print(f"lead Actor FirstName: {leadActorFirstName}")
            print(f"lead Actor LastName: {leadActorLastName}")
            print("")

    # Note: we will implement by wrapping the repository methods.
    # later if we wanted to we can easily change this to act as a microservice by replacing the repositories with
    # calls to a REST API.
    def addMovie(self, movie: Movie):
        """
        Adds a Movie object to the database.
        """
        MovieRepository().add(movie)

    def addDirector(self, director: Director):
        """
        Adds a Director object to the database.
        """
        DirectorRepository().add(director)

    def addActor(self, actor: Actor):
        """
        Adds an Actor object to the database.
        """
        ActorRepository().add(actor)


if __name__ == '__main__':
    movieDiscovery = MovieDiscovery()
    movieDiscovery.startDiscovery()