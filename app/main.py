from fastapi import FastAPI

from app.router.auth import router as auth_router
from app.router.users import router as users_router
from app.router.studies import router as studies_router


app = FastAPI(title="Study Record API")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(studies_router)