from playlist_builder.accessor import MusicPlatformDAO
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from rich import print


YOUTUBE_SERVICE_NAME = "youtube"
API_VERSION = "v3"


class YoutubeDAO(MusicPlatformDAO):
    """Accessor to interact with Youtube Data API"""

    def __init__(self):
        self.youtube_client = None
        self.credential = None

    def login(self):
        if not self.__check_if_credential_is_valid():
            print("[bold red]No valid credential available, require login.[/bold red]")
            flow = InstalledAppFlow.from_client_config(
                self.__get_client_config(),
                scopes=["https://www.googleapis.com/auth/youtube.force-ssl"],
                redirect_uri="urn:ietf:wg:oauth:2.0:oob",
            )
            self.credential = flow.run_local_server()
        else:
            print(
                "[bold green]Credential still valid, no log in required.[/bold green]"
            )
        self.youtube_client = build(
            YOUTUBE_SERVICE_NAME, API_VERSION, credentials=self.credential
        )

    def get_playlist(self):
        pass

    def add_to_playlist(self):
        pass

    def __check_if_credential_is_valid(self):
        return self.credential is not None and self.credential.valid is True

    def __get_client_config(self):
        return {
            "installed": {
                "client_id": "215067772194-jjlvof9v9hmiktad143eocrk69cdompp.apps.googleusercontent.com",
                "project_id": "playlistbuildertest",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": "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",
                "redirect_uris": ["http://localhost"],
            }
        }
