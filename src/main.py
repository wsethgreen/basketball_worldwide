import uvicorn

from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse

from src.api.health import health_router
from src.api.v1.league import league_router
from src.api.v1.simulate import simulate_router
from src.api.v1.team import team_router


app = FastAPI()

v1 = APIRouter(prefix="/v1")
v1.include_router(league_router)
v1.include_router(simulate_router)
v1.include_router(team_router)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


app.include_router(health_router)
app.include_router(v1)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
