from typing import List, Dict, Any, Optional

from pydantic import model_validator

from playlist_builder.models import Playlist, MusicBaseModel


class PageInfo(MusicBaseModel):
    total_results: int
    results_per_page: int


class YoutubePlaylist(Playlist):

    @model_validator(mode="before")
    @classmethod
    def extract_details(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        snippet = data.get("snippet", {})
        content_details = data.get("contentDetails", {})
        return {
            "id": data.get("id"),
            "title": snippet.get("title"),
            "description": snippet.get("description"),
            "itemCount": content_details.get("itemCount"),
        }


class YouTubeListAPIResponse(MusicBaseModel):
    kind: str
    etag: str
    next_page_token: Optional[str] = None
    prev_page_token: Optional[str] = None
    page_info: PageInfo
    items: List[YoutubePlaylist]
