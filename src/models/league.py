from pydantic import BaseModel


class League(BaseModel):
    id: str | int  # TODO: determine type
    name: str
