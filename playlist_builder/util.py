import json
import os
from typing import Optional
from google.oauth2.credentials import Credentials
from rich import print

from playlist_builder.constants import BASE_FILE_PATH
from playlist_builder.enums import Platform


def get_existing_credential(platform: Platform) -> Optional[Credentials]:
    try:
        file_path = os.path.join(BASE_FILE_PATH, platform.value)
        with open(file_path, "r", encoding="utf-8") as cache_file:
            existing_credential_json = json.load(cache_file)
            if platform == Platform.YOUTUBE:
                youtube_credential = json.loads(
                    existing_credential_json[platform.value]
                )
                return Credentials.from_authorized_user_info(
                    youtube_credential,
                    scopes=["https://www.googleapis.com/auth/youtube.force-ssl"],
                )
            return None
    except Exception as e:
        print(f"Failed to get cached credential for {platform.value} {e}")
        return None


def save_info_to_cache_file(platform: Platform, credentials: Credentials) -> None:
    file_path = os.path.join(BASE_FILE_PATH, platform.value)
    print("Saving credential info into cache")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as cache_file:
        json.dump(
            {platform.value: credentials.to_json()},
            cache_file,
            indent=4,
        )
