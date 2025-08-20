# backend/app/tasks.py

from .celery_worker import celery_app
from sqlalchemy.orm import sessionmaker
from .database import engine
from .models import FileRecord
import time
import pandas as pd
import os
import json

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@celery_app.task
def parse_file_task(file_id, file_path):
    session = SessionLocal()
    try:
        # Update status to 'processing'
        file_record = session.query(FileRecord).filter(FileRecord.id == file_id).first()
        file_record.status = 'processing'
        file_record.progress = 0
        session.commit()

        # Simulate parsing in chunks for progress reporting
        # (Example: CSV, but adjust as needed)
        total_lines = sum(1 for _ in open(file_path))
        chunk_size = max(total_lines // 10, 1)  # Divide into ten for demo; handle small files

        parsed_data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f):
                # Simulate complex parsing:
                parsed_data.append(line.strip().split(','))
                if idx % chunk_size == 0 or idx == total_lines - 1:
                    # Update progress
                    progress = min(100, int(100 * (idx + 1) / total_lines))
                    file_record.progress = progress
                    session.commit()
                    time.sleep(0.2)  # Simulate slow processing (remove in production)

        # Save parsed data (example: list of lists, or as needed)
        file_record.parsed_json = json.dumps(parsed_data)
        file_record.status = 'ready'
        file_record.progress = 100
        session.commit()
    except Exception as ex:
        # On error, set failed status
        file_record.status = 'failed'
        file_record.progress = 0
        session.commit()
        print(f"Error processing file {file_id}: {ex}")
    finally:
        session.close()
