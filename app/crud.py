from sqlalchemy.orm import Session
from app.models import StudyRecord
from app.schemas import StudyCreate, StudyUpdate


def create_record(
    db: Session,
    study: StudyCreate
):
    record = StudyRecord(
        subject=study.subject,
        hours=study.hours,
        memo=study.memo,
    )
    
    db.add(record)
    db.commit()
    db.refresh(record)
    
    return record


def get_records(db: Session):
    return db.query(StudyRecord).all()


def update_record(
    db: Session,
    record_id: int,
    study: StudyUpdate,
):
    record = db.query(StudyRecord).filter(StudyRecord.id == record_id).first()
    
    if not record:
        return None
    
    record.subject = study.subject
    record.hours = study.hours
    record.memo = study.memo
    
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