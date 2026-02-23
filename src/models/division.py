from pydantic import BaseModel, ConfigDict


class BaseDivision(BaseModel):
    name: str
    conference_id: int


class DivisionRead(BaseDivision):
    model_config = ConfigDict(from_attributes=True)
    id: int


class DivisionCreate(BaseDivision):
    pass


class DivisionUpdate(BaseModel):
    name: str
