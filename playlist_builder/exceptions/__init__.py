class BadInputException(Exception):
    """Exception raised when input is invalid."""

    def __init__(self, message: str):
        super(BadInputException, self).__init__(message)


class ResourceNotFoundException(Exception):
    """Exception to be thrown when a resource is not found."""

    def __init__(self, message):
        super(ResourceNotFoundException, self).__init__(message)


class PlaylistNotFoundException(ResourceNotFoundException):
    """Exception to be thrown when a playlist is not found."""

    def __init__(self, message):
        super(PlaylistNotFoundException, self).__init__(message)
