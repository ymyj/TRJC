from app.models import TaskPlot, TaskPlotStatus, TaskInfo

def try_complete_task(db, task_id):
    """
    Check if all plots under a task are completed. If so, update task status to 'completed'.
    """
    all_plots = db.query(TaskPlot).filter(TaskPlot.RWID == task_id, TaskPlot.SFSC == 0).all()
    if not all_plots:
        return

    completed_count = 0
    for tp in all_plots:
        status_record = db.query(TaskPlotStatus).filter(
            TaskPlotStatus.RWID == task_id,
            TaskPlotStatus.DKID == tp.DKID,
            TaskPlotStatus.SFSC == 0
        ).first()
        if status_record and status_record.ZT == "completed":
            completed_count += 1

    if completed_count == len(all_plots):
        task = db.query(TaskInfo).filter(TaskInfo.ID == task_id, TaskInfo.SFSC == 0).first()
        if task and task.ZT != "completed":
            task.ZT = "completed"
            db.commit()
