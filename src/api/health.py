from fastapi import APIRouter


health_router = APIRouter(prefix="/health")


@health_router.get("")
def check_health():

    return {"healthy": True}
