from urllib import parse
from typing import Dict
from click import Choice
import typer
from typing_extensions import Annotated

from playlist_builder.accessor import MusicPlatformDAO
from playlist_builder.accessor.music_platforms_dao_init import MusicPlatformsDAOInit
from playlist_builder.accessor.youtube_accessor import YoutubeDAO
from playlist_builder.enums import Platform
from rich import print

from playlist_builder.exceptions import PlaylistNotFoundException, BadInputException

playlist_builder = typer.Typer(
    no_args_is_help=True, help="Build your music playlist across platforms!"
)

music_platform_dao_init = MusicPlatformsDAOInit()
ACCESSORS: Dict[str, MusicPlatformDAO] = {Platform.YOUTUBE.value: YoutubeDAO()}


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
    accessor = music_platform_dao_init.login(platform)
    if accessor is not None:
        ACCESSORS[platform.value] = accessor
    continue_login = True
    while continue_login:
        continue_login = typer.confirm("Would you want to login to other platforms?")
        if continue_login:
            additional_platform_str = typer.prompt(
                text=f"For which platform? ", type=Choice([p.value for p in Platform])
            )
            music_platform_dao_init.login(Platform(additional_platform_str))


@playlist_builder.command()
def build(
        platform: Annotated[
            Platform,
            typer.Option(
                prompt="Please choose the platform to log into",
                help="The music platform to log into",
            ),
        ],
        new: Annotated[
            bool,
            typer.Option(
                prompt="Would you like to build a new playlist?",
                help="Choice whether to make a new playlist",
            ),
        ],
):
    playlist = None
    if new:
        # Create a new playlist
        pass
    else:
        playlist_id = None
        match platform:
            case Platform.YOUTUBE:
                playlist_url = typer.prompt(
                    "Please provide the Youtube playlist url", type=str
                )
                playlist_id = extract_youtube_playlist_id(playlist_url)

        try:
            playlist = ACCESSORS[platform.value].get_playlist(playlist_id)
            print(
                f"[green]Fetched YouTube playlist with title [bold]{playlist.title}[/bold][/green] and [bold]{playlist.item_count}[/bold]"
            )
        except PlaylistNotFoundException:
            print(
                f"[red]Playlist was not found with id: [bold]{playlist_id}[/bold][/red]"
            )
            return


def extract_youtube_playlist_id(url: str) -> str:
    url_data = parse.urlparse(url)

    # Ensure the URL is of the correct format
    if url_data.scheme != "https" or url_data.netloc != "www.youtube.com":
        raise BadInputException(f"Invalid YouTube URL format: {url}")

    query_params = parse.parse_qs(url_data.query)
    playlist_id = query_params.get("list", None)

    if not playlist_id:
        raise BadInputException(f"No playlist ID found in URL: {url}")

    return playlist_id[0]


if __name__ == "__main__":
    playlist_builder()
