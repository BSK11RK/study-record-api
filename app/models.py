from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class StudyRecord(Base):
    __tablename__ = "study_records"
    
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    hours = Column(Integer, nullable=False)
    memo = Column(String, nullable=True)
    study_date = Column(Date, nullable=False)