from playlist_builder.accessor.youtube_accessor import YoutubeDAO
from playlist_builder.enums import Platform
from rich import print


class MusicPlatformsDAO:

    def __init__(self):
        self.accessors = {Platform.YOUTUBE: YoutubeDAO(), Platform.SPOTIFY: None}

    def login(self, platform):
        try:
            self.accessors[platform].login()
            print(
                f"[bold green]Log in successful for [bold cyan]{platform.value}[/bold cyan][/bold green]"
            )
        except Exception as e:
            print(
                f"[bold red]Log in failed for [bold cyan]{platform.value}[/bold cyan]: {e}[/bold red]"
            )

    def get_playlist(self, platform, title):
        pass
