from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import TaskPlot, TaskPlotStatus, TaskInfo, PlotInfo, SurveyRecord, SampleRecord, TaskAssign, PersonInfo
from app.utils.crypto import decrypt_data
from app.utils.task_helper import try_complete_task
from app.utils.dataset_helper import _create_dataset_from_completed_plot
from typing import Optional

router = APIRouter(prefix="/api/tasks/{task_id}/plots", tags=["任务地块管理"])


@router.get("", response_model=dict)
def get_task_plots(task_id: int, ryid: Optional[int] = Query(None, description="按用户过滤地块"), db: Session = Depends(get_db)):
    print(f"[DEBUG] get_task_plots: task_id={task_id}, ryid={ryid}")
    task = db.query(TaskInfo).filter(TaskInfo.ID == task_id, TaskInfo.SFSC == 0).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    task_plots = db.query(TaskPlot).filter(TaskPlot.RWID == task_id, TaskPlot.SFSC == 0).all()
    print(f"[DEBUG] task_plots count: {len(task_plots)}")

    if ryid:
        assigned_plot_ids = db.query(TaskAssign.DKID).filter(
            TaskAssign.RWID == task_id,
            TaskAssign.RYID == ryid,
            TaskAssign.SFSC == 0
        ).all()
        assigned_plot_ids = set(row[0] for row in assigned_plot_ids)
        print(f"[DEBUG] assigned_plot_ids for ryid={ryid}: {assigned_plot_ids}")
        task_plots = [tp for tp in task_plots if tp.DKID in assigned_plot_ids]
        print(f"[DEBUG] filtered task_plots count: {len(task_plots)}")
    status_map = {s.DKID: s for s in db.query(TaskPlotStatus).filter(TaskPlotStatus.RWID == task_id, TaskPlotStatus.SFSC == 0).all()}

    result = []
    for tp in task_plots:
        plot = db.query(PlotInfo).filter(PlotInfo.ID == tp.DKID, PlotInfo.SFSC == 0).first()
        if not plot:
            continue

        status = status_map.get(tp.DKID)
        status_code = status.ZT if status else "pending"

        status_label_map = {
            "pending": "待领取",
            "sampling": "待采样",
            "transport": "待运输",
            "analysis": "待分析",
            "completed": "已完成"
        }

        survey_record = db.query(SurveyRecord).filter(SurveyRecord.RWID == task_id, SurveyRecord.DKID == tp.DKID, SurveyRecord.SFSC == 0).first()
        sample_record = db.query(SampleRecord).filter(SampleRecord.RWID == task_id, SampleRecord.DKID == tp.DKID, SampleRecord.SFSC == 0).first()

        # 从 TaskAssign 获取采样人员（按地块过滤）
        assigns = db.query(TaskAssign).filter(
            TaskAssign.RWID == task_id,
            TaskAssign.DKID == tp.DKID,
            TaskAssign.SFSC == 0
        ).all()
        samplers = []
        for a in assigns:
            person = db.query(PersonInfo).filter(PersonInfo.ID == a.RYID, PersonInfo.SFSC == 0).first()
            if person:
                samplers.append(decrypt_data(person.XM))

        result.append({
            "id": plot.ID,
            "taskName": task.RWMC,
            "code": plot.TBH,
            "unit": plot.SSDY,
            "area": float(plot.TBMJ) if plot.TBMJ else None,
            "location": plot.SSQH,
            "longitude": float(plot.JD) if plot.JD else None,
            "latitude": float(plot.WD) if plot.WD else None,
            "status": status_code,
            "statusLabel": status_label_map.get(status_code, "待领取"),
            "hasSurvey": survey_record is not None,
            "hasSample": sample_record is not None,
            "surveyTime": survey_record.KCRQ.isoformat() if survey_record and survey_record.KCRQ else None,
            "sampleTime": sample_record.CYRQ.isoformat() if sample_record and sample_record.CYRQ else None,
            "samplers": ",".join(samplers) if samplers else "",
        })

    return {"code": 200, "data": result}


@router.get("/{plot_id}", response_model=dict)
def get_task_plot_detail(task_id: int, plot_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskInfo).filter(TaskInfo.ID == task_id, TaskInfo.SFSC == 0).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    task_plot = db.query(TaskPlot).filter(TaskPlot.RWID == task_id, TaskPlot.DKID == plot_id, TaskPlot.SFSC == 0).first()
    if not task_plot:
        raise HTTPException(status_code=404, detail="地块不在该任务中")

    plot = db.query(PlotInfo).filter(PlotInfo.ID == plot_id, PlotInfo.SFSC == 0).first()
    if not plot:
        raise HTTPException(status_code=404, detail="地块不存在")

    status_record = db.query(TaskPlotStatus).filter(
        TaskPlotStatus.RWID == task_id,
        TaskPlotStatus.DKID == plot_id,
        TaskPlotStatus.SFSC == 0
    ).first()
    status_code = status_record.ZT if status_record else "pending"

    status_label_map = {
        "pending": "待领取",
        "sampling": "待采样",
        "transport": "待运输",
        "analysis": "待分析",
        "completed": "已完成"
    }

    assigns = db.query(TaskAssign).filter(
        TaskAssign.RWID == task_id,
        TaskAssign.DKID == plot_id,
        TaskAssign.SFSC == 0
    ).all()
    samplers = []
    for a in assigns:
        person = db.query(PersonInfo).filter(PersonInfo.ID == a.RYID, PersonInfo.SFSC == 0).first()
        if person:
            samplers.append(decrypt_data(person.XM))

    return {
        "code": 200,
        "data": {
            "ID": plot.ID,
            "taskName": task.RWMC,
            "code": plot.TBH,
            "unit": plot.SSDY,
            "area": float(plot.TBMJ) if plot.TBMJ else None,
            "district": plot.SSQH,
            "longitude": float(plot.JD) if plot.JD else None,
            "latitude": float(plot.WD) if plot.WD else None,
            "status": status_code,
            "statusLabel": status_label_map.get(status_code, "待领取"),
            "samplers": ",".join(samplers) if samplers else "",
        }
    }


@router.put("/{plot_id}/status", response_model=dict)
def update_plot_status(task_id: int, plot_id: int, data: dict, db: Session = Depends(get_db)):
    task = db.query(TaskInfo).filter(TaskInfo.ID == task_id, TaskInfo.SFSC == 0).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    task_plot = db.query(TaskPlot).filter(TaskPlot.RWID == task_id, TaskPlot.DKID == plot_id, TaskPlot.SFSC == 0).first()
    if not task_plot:
        raise HTTPException(status_code=404, detail="地块不在该任务中")

    status_record = db.query(TaskPlotStatus).filter(
        TaskPlotStatus.RWID == task_id,
        TaskPlotStatus.DKID == plot_id,
        TaskPlotStatus.SFSC == 0
    ).first()

    new_status = data.get("status")
    if not new_status:
        raise HTTPException(status_code=400, detail="缺少状态参数")

    if status_record:
        status_record.ZT = new_status
        if new_status == "sampling":
            status_record.KCFSJ = datetime.now()
        elif new_status == "transport":
            status_record.KCFSJ = datetime.now()
        elif new_status == "analysis":
            status_record.CYFSJ = datetime.now()
        elif new_status == "completed":
            status_record.KCFSJ = status_record.KCFSJ or datetime.now()
            status_record.CYFSJ = datetime.now()
    else:
        status_record = TaskPlotStatus(
            RWID=task_id,
            DKID=plot_id,
            ZT=new_status,
            KCFSJ=datetime.now() if new_status in ["sampling", "transport"] else None,
            CYFSJ=datetime.now() if new_status in ["analysis", "completed"] else None,
        )
        db.add(status_record)

    db.commit()

    if new_status == "completed":
        _create_dataset_from_completed_plot(db, task_id, plot_id)

    try_complete_task(db, task_id)

    return {"code": 200, "msg": "更新成功"}
