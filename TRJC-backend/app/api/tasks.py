from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.models import TaskInfo, TaskPlot, TaskPlotStatus, TaskAssign, PlotInfo, PersonInfo, SurveyRecord, SampleRecord
from app.schemas.task import TaskInfoCreate, TaskInfoUpdate, TaskInfoResponse, TaskStatsResponse
from app.utils.code_generator import generate_task_number

router = APIRouter(prefix="/api/tasks", tags=["任务管理"])


@router.get("", response_model=dict)
def get_task_list(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    keyword: Optional[str] = None,
    zt: Optional[str] = None,
    ssqh: Optional[str] = None,
    ryid: Optional[int] = None,  # 添加按人员ID过滤参数
    db: Session = Depends(get_db)
):
    base_query = db.query(TaskInfo).filter(TaskInfo.SFSC == 0)

    if keyword:
        base_query = base_query.filter(TaskInfo.RWMC.like(f"%{keyword}%"))
    if zt:
        base_query = base_query.filter(TaskInfo.ZT == zt)
    if ssqh:
        base_query = base_query.filter(TaskInfo.SSQH == ssqh)

    # 如果提供了人员ID，则只返回分配给该人员的任务
    if ryid:
        assigned_task_ids = db.query(TaskAssign.RWID).filter(
            TaskAssign.RYID == ryid,
            TaskAssign.SFSC == 0
        ).subquery()
        base_query = base_query.filter(TaskInfo.ID.in_(assigned_task_ids))

    query = base_query
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()

    result = []
    for item in items:
        assignees = db.query(TaskAssign).filter(TaskAssign.RWID == item.ID, TaskAssign.SFSC == 0).all()
        result.append({
            "ID": item.ID,
            "RWBH": item.RWBH,
            "RWMC": item.RWMC,
            "RWLX": item.RWLX,
            "SSQH": item.SSQH,
            "FZR": item.FZR,
            "ZT": item.ZT,
            "CJSJ": item.CJSJ,
            "assignee_count": len(assignees)
        })

    return {"code": 200, "data": {"list": result, "total": total, "page": page, "size": size}}


@router.get("/stats", response_model=dict)
def get_task_stats(db: Session = Depends(get_db)):
    total = db.query(TaskInfo).filter(TaskInfo.SFSC == 0).count()
    pending = db.query(TaskInfo).filter(TaskInfo.SFSC == 0, TaskInfo.ZT == "pending").count()
    processing = db.query(TaskInfo).filter(TaskInfo.SFSC == 0, TaskInfo.ZT == "processing").count()
    completed = db.query(TaskInfo).filter(TaskInfo.SFSC == 0, TaskInfo.ZT == "completed").count()

    return {"code": 200, "data": {"total": total, "pending": pending, "processing": processing, "completed": completed}}


@router.post("", response_model=dict)
def create_task(data: TaskInfoCreate, db: Session = Depends(get_db)):
    task_no = generate_task_number(db)

    ssql = data.SSQH
    if not ssql and data.plot_ids:
        from app.models import PlotInfo
        plots = db.query(PlotInfo).filter(PlotInfo.ID.in_(data.plot_ids), PlotInfo.SFSC == 0).all()
        if plots:
            districts = list(set(p.SSQH for p in plots if p.SSQH))
            if districts:
                ssql = districts[0] if len(districts) == 1 else ",".join(districts)

    db_item = TaskInfo(
        RWBH=task_no,
        RWMC=data.RWMC,
        RWLX=data.RWLX,
        SSQH=ssql,
        FZR=data.FZR,
        JHKSSJ=data.JHKSSJ,
        LXDH=data.LXDH,
        RWMS=data.RWMS,
        ZT="pending"
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    if data.plot_ids:
        for plot_id in data.plot_ids:
            task_plot = TaskPlot(RWID=db_item.ID, DKID=plot_id)
            db.add(task_plot)
        db.commit()

    return {"code": 200, "msg": "创建成功", "data": {"ID": db_item.ID, "RWBH": task_no}}


@router.post("/{task_id}/assign", response_model=dict)
def assign_task(task_id: int, personnel_ids: List[int], db: Session = Depends(get_db)):
    task = db.query(TaskInfo).filter(TaskInfo.ID == task_id, TaskInfo.SFSC == 0).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    for person_id in personnel_ids:
        existing = db.query(TaskAssign).filter(TaskAssign.RWID == task_id, TaskAssign.RYID == person_id, TaskAssign.SFSC == 0).first()
        if not existing:
            assign = TaskAssign(RWID=task_id, RYID=person_id)
            db.add(assign)

    task.ZT = "processing"
    db.commit()
    return {"code": 200, "msg": "分配成功"}


@router.put("/{task_id}", response_model=dict)
def update_task(task_id: int, data: TaskInfoUpdate, db: Session = Depends(get_db)):
    item = db.query(TaskInfo).filter(TaskInfo.ID == task_id, TaskInfo.SFSC == 0).first()
    if not item:
        raise HTTPException(status_code=404, detail="任务不存在")

    if data.RWMC is not None:
        item.RWMC = data.RWMC
    if data.RWLX is not None:
        item.RWLX = data.RWLX
    if data.SSQH is not None:
        item.SSQH = data.SSQH
    if data.FZR is not None:
        item.FZR = data.FZR
    if data.ZT is not None:
        item.ZT = data.ZT

    if data.plot_ids is not None:
        db.query(TaskPlot).filter(TaskPlot.RWID == task_id).delete()
        for plot_id in data.plot_ids:
            task_plot = TaskPlot(RWID=task_id, DKID=plot_id)
            db.add(task_plot)

    db.commit()
    return {"code": 200, "msg": "更新成功"}


@router.delete("/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    item = db.query(TaskInfo).filter(TaskInfo.ID == task_id, TaskInfo.SFSC == 0).first()
    if not item:
        raise HTTPException(status_code=404, detail="任务不存在")

    item.SFSC = 1
    db.commit()
    return {"code": 200, "msg": "删除成功"}


@router.get("/{task_id}", response_model=dict)
def get_task_detail(task_id: int, db: Session = Depends(get_db)):
    item = db.query(TaskInfo).filter(TaskInfo.ID == task_id, TaskInfo.SFSC == 0).first()
    if not item:
        raise HTTPException(status_code=404, detail="任务不存在")

    plots = db.query(TaskPlot).filter(TaskPlot.RWID == task_id, TaskPlot.SFSC == 0).all()
    plot_ids = [p.DKID for p in plots]
    
    status_map = {s.DKID: s for s in db.query(TaskPlotStatus).filter(TaskPlotStatus.RWID == task_id, TaskPlotStatus.SFSC == 0).all()}
    
    plot_details = []
    if plot_ids:
        plot_objs = db.query(PlotInfo).filter(PlotInfo.ID.in_(plot_ids), PlotInfo.SFSC == 0).all()
        for p in plot_objs:
            status_record = status_map.get(p.ID)
            status_code = status_record.ZT if status_record else "pending"
            plot_details.append({
                "ID": p.ID,
                "TBH": p.TBH,
                "SSDY": p.SSDY,
                "TBMJ": float(p.TBMJ) if p.TBMJ else None,
                "SSQH": p.SSQH,
                "JD": float(p.JD) if p.JD else None,
                "WD": float(p.WD) if p.WD else None,
                "WLZB": p.WLZB,
                "CJSJ": p.CJSJ.strftime("%Y-%m-%d %H:%M:%S") if p.CJSJ else None,
                "status": status_code,
                "statusLabel": {"pending": "待领取", "sampling": "待采样", "transport": "待运输", "analysis": "待分析", "completed": "已完成"}.get(status_code, "待领取")
            })

    assignees = db.query(TaskAssign).filter(TaskAssign.RWID == task_id, TaskAssign.SFSC == 0).all()
    assignee_ids = [a.RYID for a in assignees]

    contact = None
    if item.FZR:
        person = db.query(PersonInfo).filter(PersonInfo.XM == item.FZR, PersonInfo.SFSC == 0).first()
        if person and person.LXFS:
            from app.utils.crypto import decrypt_data
            contact = decrypt_data(person.LXFS)

    survey = db.query(SurveyRecord).filter(SurveyRecord.RWID == task_id, SurveyRecord.SFSC == 0).first()
    sample = db.query(SampleRecord).filter(SampleRecord.RWID == task_id, SampleRecord.SFSC == 0).first()

    return {
        "code": 200,
        "data": {
            "ID": item.ID,
            "RWBH": item.RWBH,
            "RWMC": item.RWMC,
            "RWLX": item.RWLX,
            "SSQH": item.SSQH,
            "FZR": item.FZR,
            "JHKSSJ": item.JHKSSJ,
            "LXDH": item.LXDH,
            "RWMS": item.RWMS,
            "ZT": item.ZT,
            "CJSJ": item.CJSJ.strftime("%Y-%m-%d %H:%M:%S") if item.CJSJ else None,
            "plot_ids": plot_ids,
            "plots": plot_details,
            "assignee_ids": assignee_ids,
            "survey_id": survey.ID if survey else None,
            "sample_id": sample.ID if sample else None
        }
    }
