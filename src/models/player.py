from datetime import datetime
from pydantic import BaseModel


# TODO: determine player model
class Player(BaseModel):
    id: str
    name: str
    age: int
    dob: datetime  # could be fun to have dobs?
    team_id: str | int  # what should team ID types be?
