from typing import Optional
from playlist_builder.accessor import MusicPlatformDAO
from playlist_builder.accessor.youtube_accessor import YoutubeDAO
from playlist_builder.enums import Platform
from rich import print


class MusicPlatformsDAOInit:

    def __init__(self):
        self.accessors_init = {Platform.YOUTUBE: YoutubeDAO, Platform.SPOTIFY: None}

    def login(self, platform) -> Optional[MusicPlatformDAO]:
        try:
            accessor = self.accessors_init[platform].login()
            print(
                f"[bold green]Log in successful for [bold cyan]{platform.value}[/bold cyan][/bold green]"
            )
            return accessor
        except Exception as e:
            print(
                f"[bold red]Log in failed for [bold cyan]{platform.value}[/bold cyan]: {e}[/bold red]"
            )

        return None
