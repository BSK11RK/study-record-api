from fastapi import FastAPI
from app.router.studies import router as studies_router


app = FastAPI(title="Study Record API")

app.include_router(studies_router)