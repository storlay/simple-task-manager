from fastapi import APIRouter

from src.api.task import router as task_router


routers = (task_router,)


main_router = APIRouter()


for router in routers:
    main_router.include_router(router)
