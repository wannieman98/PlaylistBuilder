from click import Choice
import typer
from typing_extensions import Annotated

from playlist_builder.accessor.music_platform_dao import MusicPlatformsDAO
from playlist_builder.accessor.youtube_accessor import YoutubeDAO
from playlist_builder.enums import Platform
from rich import print


playlist_builder = typer.Typer(
    no_args_is_help=True, help="Build your music playlist across platforms!"
)

platforms_dao = MusicPlatformsDAO()


@playlist_builder.command()
def login(
    platform: Annotated[
        Platform,
        typer.Option(
            prompt="Please choose the platform to log into",
            help="The music platform to log into",
        ),
    ]
):
    """
    Log in to music platforms to build and sync playlists

    If --platform is not specified you will be prompted to select one.
    """
    platforms_dao.login(platform)
    continue_login = True
    while continue_login:
        continue_login = typer.confirm("Would you want to login to other platforms?")
        if continue_login:
            additional_platform_str = typer.prompt(
                text=f"For which platform? ", type=Choice([p.value for p in Platform])
            )
            platforms_dao.login(Platform(additional_platform_str))


@playlist_builder.command()
def build():
    # 1. Ask user if they want to create a new playlist
    #  1-1. If no, provide playlist link
    #  1-2. Else, what is the title and privacy etc,..
    # 2. What to build from? E.G., youtube video or another platform's playlist
    pass


if __name__ == "__main__":
    playlist_builder()
