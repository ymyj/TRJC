import time
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from app.models import TaskInfo


def generate_task_number(db: Session) -> str:
    year = datetime.now().strftime("%Y")
    prefix = f"RW{year}"

    result = db.query(func.max(TaskInfo.RWBH)).filter(
        TaskInfo.RWBH.like(f"{prefix}%")
    ).first()

    if result and result[0]:
        max_no = int(result[0].replace(prefix, ""))
        new_no = max_no + 1
    else:
        new_no = 1

    return f"{prefix}{new_no:05d}"
