import requests
import logging


class GuideboxAPI:
    """Used to fetch data from the Guidebox API"""

    def get_url(*paths):
        """
        Return an http url/path from the given path components
        :param paths: Paths to join
        :return: http path
        """
        clean_paths = [x.strip('/') for x in paths]
        return '/'.join(clean_paths)

    __INDEX_NAME = 'conflux'
    __TYPE_MOVIES = 'movies'
    __GUIDEBOX_HOST = 'https://api-public.guidebox.com'
    __GUIDEBOX_VER = 'v1.43'
    __GUIDEBOX_REGION_US = 'US'
    __GUIDEBOX_API_KEY = 'rKaLPYRwwXYRIwNHYtcEXTvbvlaicfra'
    __GUIDEBOX_BASE_PATH = get_url(__GUIDEBOX_HOST, __GUIDEBOX_VER, __GUIDEBOX_REGION_US, __GUIDEBOX_API_KEY)
    __GUIDEBOX_MOVIES_PATH = get_url(__GUIDEBOX_BASE_PATH, 'movies')
    __GUIDEBOX_MOVIES_ALL_PATH = get_url(__GUIDEBOX_MOVIES_PATH, 'all')
    __GUIDEBOX_MOVIE_PATH = get_url(__GUIDEBOX_BASE_PATH, 'movie')
    __GUIDEBOX_UPDATES_PATH = get_url(__GUIDEBOX_BASE_PATH, 'updates')
    __GUIDEBOX_UPDATES_MOVIES_PATH = get_url(__GUIDEBOX_UPDATES_PATH, 'movies')
    __GUIDEBOX_MOVIES_CHANGES_PATH = get_url(__GUIDEBOX_UPDATES_MOVIES_PATH, 'changes')
    __GUIDEBOX_NEW_MOVIES_PATH = get_url(__GUIDEBOX_UPDATES_MOVIES_PATH, 'new')
    __GUIDEBOX_DELETED_MOVIES_PATH = get_url(__GUIDEBOX_UPDATES_MOVIES_PATH, 'deletes')
    __GUIDEBOX_TIME_PATH = get_url(__GUIDEBOX_UPDATES_PATH, 'get_current_time')

    logger = logging.getLogger(__name__)

    def get_timestamp(self):
        """Retrieve the current UNIX timestamp from Guidebox"""
        self.logger.info('Guidebox get_timestamp')
        self.logger.info('GET %s', self.__GUIDEBOX_TIME_PATH)
        response = requests.get(self.__GUIDEBOX_TIME_PATH)
        if response.ok:
            return response.json()
        else:
            self.logger.error('Error retrieving timestamp')
            response.raise_for_status()

    def get_movies(self, start, size):
        """
        Retrieve most popular movies from Guidebox
        :param start: Starting index of movies to retrieve
        :param size: Number of movies to retrieve, starting at 'start'
        :return: Guidebox movies API response in JSON dict
        """
        self.logger.info('Guidebox get_movies %d-%d (%d movies)', start, start + size, size)
        url = GuideboxAPI.get_url(self.__GUIDEBOX_MOVIES_ALL_PATH, str(start), str(size))
        self.logger.info("GET %s", url)
        response = requests.get(url)
        if response.ok:
            movies = response.json()
            self.logger.info('Successfully retrieved %d movies', movies['total_returned'])
            return movies
        else:
            self.logger.error('Guidebox movies call failure. Response: %s', response)
            response.raise_for_status()

    def get_movie(self, movie_id):
        """
        Retrieve movie with given id
        :param movie_id: ID of movie to retrieve
        :return: Guidebox movie API response in JSON dict
        """
        self.logger.info('Guidebox get_movie: %d', movie_id)
        url = GuideboxAPI.get_url(self.__GUIDEBOX_MOVIE_PATH, str(movie_id))
        self.logger.info('GET %s', url)
        response = requests.get(url)
        if response.ok:
            movie_data = response.json()
            self.logger.info('Successfully retrieved movie %s: %s', movie_data['id'], movie_data['title'])
            return movie_data
        else:
            self.logger.error('Error retrieving movie %s. Response: %s', movie_id, response)
            response.raise_for_status()

    def get_movie_changes(self, since):
        """
        Retrieve movies that have changed since 'since' timestamp
        :param since: UNIX timestamp of last update, as retrieved from Guidebox
        :return: Guidebox movie changes API response in JSON dict
        """
        self.logger.info('Guidebox get_movie_changes (since: %s)', since)
        url = GuideboxAPI.get_url(self.__GUIDEBOX_MOVIES_CHANGES_PATH, since)
        self.logger.info('GET %s', url)
        response = requests.get(url)
        if response.ok:
            movie_changes = response.json()
            self.logger.info('Successfully retrieved %d of %d movie changes', movie_changes['total_returned'],
                             movie_changes['total_results'])
            return movie_changes
        else:
            self.logger.error('Error retrieving movie changes. Response: %s', response)
            response.raise_for_status()

    def get_new_movies(self, since):
        """
        Retrieve movies that have been added since 'since' timestamp
        :param since: UNIX timestamp of last update, as retrieved from Guidebox
        :return: Guidebox new movies API response in JSON dict
        """
        self.logger.info('Guidebox get_new_movies (since: %s)', since)
        url = GuideboxAPI.get_url(self.__GUIDEBOX_NEW_MOVIES_PATH, since)
        self.logger.info('GET %s', url)
        response = requests.get(url)
        if response.ok:
            new_movies = response.json()
            self.logger.info('Successfully retrieved %d of %d new movies', new_movies['total_returned'],
                             new_movies['total_results'])
            return new_movies
        else:
            self.logger.error('Error retrieving new movies. Response: %s', response)
            response.raise_for_status()

    def get_deleted_movies(self, since):
        """
        Retrieve movies that have been deleted since 'since' timestamp
        :param since: UNIX timestamp of last update, as retrieved from Guidebox
        :return: Guidebox deleted movies API response in JSON dict
        """
        self.logger.info('Guidebox get_deleted_movies (since: %s)', since)
        url = GuideboxAPI.get_url(self.__GUIDEBOX_DELETED_MOVIES_PATH, since)
        self.logger.info('GET %s', url)
        response = requests.get(url)
        if response.ok:
            deleted_movies = response.json()
            self.logger.info('Successfully retrieved %d of %d new movies', deleted_movies['total_returned'],
                             deleted_movies['total_results'])
            return deleted_movies
        else:
            self.logger.error('Error retrieving deleted movies. Response: %s', response)
            response.raise_for_status()
