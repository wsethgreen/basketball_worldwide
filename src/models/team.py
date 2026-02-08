from pydantic import BaseModel


class Team(BaseModel):
    id: str | int  # TODO: determine type
    name: str
    league_id: str | int  # TODO: determine type
