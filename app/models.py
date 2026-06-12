from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    studies = relationship("StudyRecord", back_populates="user")
    
    
class Follow(Base):
    __tablename__ = "follows"
    
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    following_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class StudyRecord(Base):
    __tablename__ = "study_records"
    
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    hours = Column(Integer, nullable=False)
    memo = Column(String, nullable=True)
    study_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="studies")