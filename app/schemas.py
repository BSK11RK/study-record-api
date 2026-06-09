from pydantic import BaseModel


class StudyCreate(BaseModel):
    subject: str
    hours: int
    memo: str | None = None
    
    
class StudyUpdate(BaseModel):
    subject: str
    hours: int
    memo: str | None = None
    
    
class StudyResponse(BaseModel):
    id: int
    subject: str
    hours: int
    memo: str | None = None
    
    class Config:
        from_attributes = True