from pydantic import BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel, to_pascal


class MusicBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
            serialization_alias=to_pascal,
        )
    )


class Playlist(MusicBaseModel):
    id: str
    title: str
    description: str
    item_count: int
