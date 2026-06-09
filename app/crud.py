from sqlalchemy.orm import Session
from app.models import StudyRecord
from app.schemas import StudyCreate, StudyPatch


def create_record(
    db: Session,
    study: StudyCreate
):
    record = StudyRecord(
        subject=study.subject,
        hours=study.hours,
        memo=study.memo,
        study_date=study.study_date,
    )
    
    db.add(record)
    db.commit()
    db.refresh(record)
    
    return record


def get_records(db: Session):
    return db.query(StudyRecord).all()


def patch_record(
    db: Session,
    record_id: int,
    study: StudyPatch,
):
    record = db.query(StudyRecord).filter(StudyRecord.id == record_id).first()
    
    if not record:
        return None
    
    update_date = study.model_dump(exclude_unset=True)
    
    for field, value in update_date.items():
        setattr(record, field, value)
    
    db.commit()
    db.refresh(record)
    
    return record


def delete_record(
    db: Session,
    record_id: int,
):
    record = db.query(StudyRecord).filter(StudyRecord.id == record_id).first()
    
    if not record:
        return False
    
    db.delete(record)
    db.commit()
    
    return True