import sys
sys.path.insert(0, r'c:\Users\Administrator\Desktop\土壤监测\土壤监测\TRJC-backend')
from app.database import SessionLocal
from app.models import TaskInfo, TaskPlot, TaskPlotStatus
from app.utils.task_helper import try_complete_task

db = SessionLocal()

# Fix existing "测试7" task
task = db.query(TaskInfo).filter(TaskInfo.RWMC.like('%测试7%')).first()
if task:
    print(f'Before: Task {task.RWMC} (ID: {task.ID}) status = {task.ZT}')
    try_complete_task(db, task.ID)
    db.refresh(task)
    print(f'After: Task {task.RWMC} (ID: {task.ID}) status = {task.ZT}')
else:
    print('Task not found')

db.close()
