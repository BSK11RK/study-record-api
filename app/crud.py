from datetime import date
from sqlalchemy import func
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


def get_records(
    db: Session,
    subject: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
):
    query = db.query(StudyRecord)
    
    if subject:
        query = query.filter(StudyRecord.subject == subject)
        
    if start_date:
        query = query.filter(StudyRecord.study_date >= start_date)
        
    if end_date:
        query = query.filter(StudyRecord.study_date <= end_date)
        
    return query.all()


def get_record_by_id(
    db: Session,
    record_id: int,
):
    return db.query(StudyRecord).filter(StudyRecord.id == record_id).first()


def get_total_hours(db: Session):
    total = db.query(func.sum(StudyRecord.hours)).scalar()
    
    return total or 0


def get_subject_summary(db: Session):
    rows = db.query(
        StudyRecord.subject, 
        func.sum(StudyRecord.hours)
    ).group_by(
        StudyRecord.subject
    ).all()


    return {
        subject: hours
        for subject, hours in rows
    }

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