from abc import ABC, abstractmethod


class MusicPlatformDAO(ABC):
    """
    Abstract Base Class for Music Platform Data Access Object (DAO)

    This class serves as a blueprint for implementing data access objects for various music platforms.
    It defines the core methods that any subclass must implement to interact with music platform services
    such as login, retrieving playlists, and adding songs to playlists.
    """

    @abstractmethod
    def login(self):
        """
        Log in to the music platform.

        This method must be implemented by subclasses to handle the authentication process
        required by the specific music platform.
        """
        ...

    @abstractmethod
    def get_playlist(self):
        """
        Retrieve a playlist from the music platform.

        This method must be implemented by subclasses to fetch playlists from the music platform.
        The exact implementation will depend on the platform's API and data structure.
        """
        ...

    @abstractmethod
    def add_to_playlist(self):
        """
        Add a song to a playlist on the music platform.

        This method must be implemented by subclasses to add songs to a playlist on the music platform.
        The implementation will depend on the platform's API for adding items to playlists.
        """
        ...
