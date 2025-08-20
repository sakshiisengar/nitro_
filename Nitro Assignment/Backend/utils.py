import os
import shutil
from sqlalchemy.orm import Session
from .models import FileRecord

UPLOAD_DIR = "uploads"

def save_upload_file(upload_file, file_id: str) -> str:
    """
    Save a starlette UploadFile to disk under uploads/ directory, 
    prefixing filename with file_id.
    Returns the path to the saved file.
    """
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{upload_file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path

def update_file_progress(db: Session, file_id: str, status: str, progress: int):
    """
    Update the progress and status of a file record in DB.
    """
    file_record = db.query(FileRecord).filter(FileRecord.id == file_id).first()
    if file_record:
        file_record.status = status
        file_record.progress = progress
        db.commit()
        db.refresh(file_record)
    return file_record
