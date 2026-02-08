import uvicorn

from fastapi import FastAPI

from api.health import health_router


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Basketball Worldwide!"}


app.include_router(health_router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
