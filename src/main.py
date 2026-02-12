import uvicorn

from faker import Faker
from fastapi import FastAPI, APIRouter

from src.api.health import health_router
from src.api.v1.league import league_router
from src.api.v1.team import team_router


app = FastAPI()

v1 = APIRouter(prefix="/v1")
v1.include_router(league_router)
v1.include_router(team_router)


@app.get("/")
async def root():
    faker = Faker()

    return {"message": "Basketball Worldwide!", "fake_name": faker.name_male()}


app.include_router(v1)
app.include_router(health_router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
