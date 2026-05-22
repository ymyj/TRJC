import sys
sys.path.insert(0, r'c:\Users\Administrator\Desktop\土壤监测\土壤监测\TRJC-backend')
from app.database import SessionLocal
from app.models import TaskInfo, TaskPlot, TaskPlotStatus

db = SessionLocal()

# Find all tasks that are in 'processing' state
tasks = db.query(TaskInfo).filter(TaskInfo.SFSC == 0, TaskInfo.ZT == 'processing').all()
print(f'Found {len(tasks)} tasks in processing state')

for task in tasks:
    print(f'\nTask: {task.RWMC} (ID: {task.ID}, Status: {task.ZT})')
    plots = db.query(TaskPlot).filter(TaskPlot.RWID == task.ID, TaskPlot.SFSC == 0).all()
    print(f'  Plots count: {len(plots)}')
    completed_count = 0
    for p in plots:
        status = db.query(TaskPlotStatus).filter(
            TaskPlotStatus.RWID == task.ID, 
            TaskPlotStatus.DKID == p.DKID, 
            TaskPlotStatus.SFSC == 0
        ).first()
        s = status.ZT if status else "no record"
        print(f'    Plot DKID: {p.DKID}, Status: {s}')
        if status and status.ZT == "completed":
            completed_count += 1
    print(f'  Completed: {completed_count}/{len(plots)}')
    if len(plots) > 0 and completed_count == len(plots):
        print(f'  >>> ALL PLOTS COMPLETED! Task should be completed!')

db.close()
