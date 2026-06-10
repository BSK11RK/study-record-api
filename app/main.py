from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import engine, SessionLocal
from app.models import Base
from app.schemas import StudyCreate, StudyResponse, StudyPatch
from app.crud import (
    create_record, 
    get_records, 
    get_record_by_id, 
    get_total_hours, 
    patch_record, 
    delete_record
)


app = FastAPI()


# テーブル作成
Base.metadata.create_all(bind=engine)


# DB接続取得
def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
        
# 学習記録追加
@app.post("/studies", response_model=StudyResponse)
def add_study(
    study: StudyCreate,
    db: Session = Depends(get_db)
):
    return create_record(db, study)


# 学習記録一覧取得
@app.get("/studies", response_model=list[StudyResponse])
def read_studies(
    subject: str | None = None,
    db: Session = Depends(get_db)
):
    return get_records(db, subject)


# 総学習時間
@app.get("/studies/total-hours")
def read_total_hours(db: Session = Depends(get_db)):
    return {"total_hours": get_total_hours(db)}


# 1件取得
@app.get("/studies/{record_id}", response_model=StudyResponse)
def read_study(
    record_id: int,
    db: Session = Depends(get_db)
):
    record = get_record_by_id(db, record_id)
    
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    return record


# 更新
@app.patch("/studies/{record_id}", response_model=StudyResponse)
def update_study(
    record_id: int,
    study: StudyPatch,
    db: Session = Depends(get_db),
):
    record = patch_record(db, record_id, study)
    
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    return record


# 削除
@app.delete("/studies/{record_id}")
def delete_study(
    record_id: int,
    db: Session = Depends(get_db),
):
    success = delete_record(db, record_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    
    return {"message": "Deleted"}