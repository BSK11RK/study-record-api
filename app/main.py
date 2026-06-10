from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.router.studies import router as studies_router


app = FastAPI(title="Study Record API")


# テーブル作成
Base.metadata.create_all(bind=engine)

app.include_router(studies_router)