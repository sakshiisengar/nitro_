from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FileBase(BaseModel):
    filename: str

class FileCreate(FileBase):
    pass  # For now no extra input fields beyond filename

class FileProgress(BaseModel):
    file_id: str
    status: str
    progress: int

class FileContent(BaseModel):
    file_id: str
    status: str
    parsed_content: Optional[List[List[str]]] = None
    message: Optional[str] = None

class FileMeta(BaseModel):
    id: str
    filename: str
    status: str
    progress: int
    created_at: datetime

    class Config:
        orm_mode = True
