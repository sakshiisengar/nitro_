import uuid
from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()
class FileRecord(Base):
    __tablename__ = "files"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String)
    status = Column(String)
    progress = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    content_path = Column(String)
parsed_json = Column(JSON, nullable=True)
