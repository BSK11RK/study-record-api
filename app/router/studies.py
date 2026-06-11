from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.auth import get_current_user
from app.models import User
from app.schemas import (
    StudyCreate, 
    StudyPatch, 
    StudyResponse,
    TimelineResponse
)
from app.crud import (
    create_record,
    get_records,
    get_record_by_id,
    get_total_hours,
    get_subject_summary,
    get_timeline,
    patch_record,
    delete_record
)


router = APIRouter(prefix="/studies", tags=["Studies"])


# DB接続取得
def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        

# 学習記録追加       
@router.post("", response_model=StudyResponse)
def add_study(
    study: StudyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_record(db, study, current_user.id)


# 学習記録一覧取得
@router.get("", response_model=list[StudyResponse])
def read_studies(
    subject: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_records(
        db, 
        current_user.id, 
        subject, 
        start_date, 
        end_date
    )


# 総学習時間
@router.get("/total-hours")
def read_total_hours(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {"total_hours": get_total_hours(db, current_user.id)}


# 科目別集計
@router.get("/summary")
def read_subject_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_subject_summary(db, current_user.id)


# タイムライン
@router.get("/timeline", response_model=list[TimelineResponse])
def read_timeline(
    db: Session = Depends(get_db),
    user_id: int | None = None,
    order: str = "desc"
):
    return get_timeline(
        db=db,
        user_id=user_id,
        order=order
    )


# 1件取得
@router.get("/{record_id}", response_model=StudyResponse)
def read_study(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = get_record_by_id(db, record_id, current_user.id)
    
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    return record


# 更新
@router.patch("/{record_id}", response_model=StudyResponse)
def update_study(
    record_id: int,
    study: StudyPatch,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = patch_record(db, record_id, current_user.id, study)
    
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    return record


# 削除
@router.delete("/{record_id}")
def delete_study(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    success = delete_record(db, record_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    
    return {"message": "deleted"}