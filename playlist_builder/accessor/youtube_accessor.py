from typing import Dict, Any

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from rich import print

from playlist_builder.accessor import MusicPlatformDAO
from playlist_builder.enums import Platform
from playlist_builder.exceptions import PlaylistNotFoundException
from playlist_builder.models.youtube_model import (
    YouTubeListAPIResponse,
    YoutubePlaylist,
)
from playlist_builder.util import get_existing_credential, save_info_to_cache_file

YOUTUBE_SERVICE_NAME = "youtube"
API_VERSION = "v3"


class YoutubeDAO(MusicPlatformDAO):
    """Accessor to interact with YouTube Data API"""

    @classmethod
    def login(cls):
        existing_credential = get_existing_credential(platform=Platform.YOUTUBE)
        if not existing_credential or not existing_credential.valid:
            print("[bold red]No valid credential available, require login.[/bold red]")
            flow = InstalledAppFlow.from_client_config(
                get_client_config(),
                scopes=["https://www.googleapis.com/auth/youtube.force-ssl"],
                redirect_uri="urn:ietf:wg:oauth:2.0:oob",
            )
            credentials = flow.run_local_server()
            save_info_to_cache_file(platform=Platform.YOUTUBE, credentials=credentials)
        else:
            print(
                "[bold green]Credential still valid, no log in required.[/bold green]"
            )

    def get_playlist(self, playlist_id: str) -> YoutubePlaylist:
        credentials = get_existing_credential(Platform.YOUTUBE)
        youtube_client = build(
            YOUTUBE_SERVICE_NAME, API_VERSION, credentials=credentials
        )
        playlist_request = youtube_client.playlists().list(
            part="snippet, contentDetails", id=playlist_id, maxResults=1
        )

        playlist_response_json = playlist_request.execute()
        playlist_response = YouTubeListAPIResponse.model_validate(
            playlist_response_json
        )

        if playlist_response.page_info.total_results < 1:
            raise PlaylistNotFoundException("There was no playlist with such Id")

        return playlist_response.items[0]

    def add_to_playlist(self):
        pass


def get_client_config() -> Dict[str, Any]:
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
