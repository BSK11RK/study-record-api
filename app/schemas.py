from pydantic import BaseModel
from datetime import date


class StudyCreate(BaseModel):
    subject: str
    hours: int
    memo: str | None = None
    study_date: date
    
    
class StudyPatch(BaseModel):
    subject: str | None = None
    hours: int | None = None
    memo: str | None = None
    study_date: date | None = None
    
    
class StudyResponse(BaseModel):
    id: int
    subject: str
    hours: int
    memo: str | None = None
    study_date: date
    
    class Config:
        from_attributes = True