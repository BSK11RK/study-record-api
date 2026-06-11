from datetime import date
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import User, StudyRecord
from app.schemas import StudyCreate, StudyPatch


# User
def create_user(
    db: Session,
    username: str,
    password: str,
):
    user = User(
        username=username,
        password=password,
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


def get_user_by_username(
    db: Session,
    username: str,
):
    return db.query(User).filter(User.username == username).first()


# Study Record
def create_record(
    db: Session,
    study: StudyCreate,
    user_id: int
):
    record = StudyRecord(
        subject=study.subject,
        hours=study.hours,
        memo=study.memo,
        study_date=study.study_date,
        user_id=user_id
    )
    
    db.add(record)
    db.commit()
    db.refresh(record)
    
    return record


def get_records(
    db: Session,
    user_id: int,
    subject: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
):
    query = db.query(StudyRecord).filter(StudyRecord.user_id == user_id)
    
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
    user_id: int
):
    return db.query(StudyRecord).filter(
        StudyRecord.id == record_id,
        StudyRecord.user_id == user_id
    ).first()


def get_total_hours(
    db: Session, 
    user_id: int
):
    total = (
        db.query(
            func.sum(StudyRecord.hours)
        )
        .filter(
            StudyRecord.user_id == user_id
        )
        .scalar()
    )
    
    return total or 0


def get_subject_summary(
    db: Session,
    user_id: int
):
    rows = (
        db.query(
            StudyRecord.subject,
            func.sum(StudyRecord.hours)
        )
        .filter(
            StudyRecord.user_id == user_id
        )
        .group_by(
            StudyRecord.subject
        )
        .all()
    )


    return {
        subject: hours
        for subject, hours in rows
    }

def patch_record(
    db: Session,
    record_id: int,
    user_id: int,
    study: StudyPatch
):
    record = (
        db.query(StudyRecord)
        .filter(
            StudyRecord.id == record_id,
            StudyRecord.user_id == user_id
        )
        .first()
    )
    
    if not record:
        return None
    
    update_data = study.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(record, field, value)
    
    db.commit()
    db.refresh(record)
    
    return record


def delete_record(
    db: Session, 
    record_id: int, 
    user_id: int
):
    record = (
        db.query(StudyRecord)
        .filter(
            StudyRecord.id == record_id,
            StudyRecord.user_id == user_id
        )
        .first()
    )
    
    if not record:
        return False
    
    db.delete(record)
    db.commit()
    
    return True


def get_timeline(
    db: Session,
    user_id: int | None = None,
    order: str = "desc",
    page: int = 1,
    size: int = 10,
):
    query = (
        db.query(
            StudyRecord,
            User.username
        )
        .join(
            User,
            StudyRecord.user_id == User.id
        )
    )
    
    if user_id:
        query = query.filter(
            StudyRecord.user_id == user_id
        )
        
    total = query.count()
        
    if order == "asc":
        query = query.order_by(
            StudyRecord.id.asc()
        )
    else:
        query = query.order_by(
            StudyRecord.id.desc()
        )
    
    records = query.offset((page - 1) * size).limit(size).all()
    
    items = []
    
    for study, username in records:
        items.append(
            {
                "id": study.id,
                "user_id": study.user_id,
                "username": username,
                "subject": study.subject,
                "hours": study.hours,
                "memo": study.memo
            }
        )
        
    return {
        "page": page,
        "size": size,
        "total": total,
        "items": items
    }