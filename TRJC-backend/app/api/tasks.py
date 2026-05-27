import time
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, case
from typing import Optional, List
from app.database import get_db
from app.models import TaskInfo, TaskPlot, TaskPlotStatus, TaskAssign, PlotInfo, PersonInfo, SurveyRecord, SampleRecord, TaskAttachment
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
    fzr: Optional[str] = None,
    rwlx: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    ryid: Optional[int] = None,
    db: Session = Depends(get_db)
):
    base_query = db.query(TaskInfo).filter(TaskInfo.SFSC == 0)

    if keyword:
        base_query = base_query.filter(TaskInfo.RWMC.like(f"%{keyword}%"))
    if zt:
        base_query = base_query.filter(TaskInfo.ZT == zt)
    if ssqh:
        base_query = base_query.filter(TaskInfo.SSQH.like(f"%{ssqh}%"))
    if fzr:
        base_query = base_query.filter(TaskInfo.FZR.like(f"%{fzr}%"))
    if rwlx:
        base_query = base_query.filter(TaskInfo.RWLX == rwlx)
    if start_time:
        base_query = base_query.filter(TaskInfo.CJSJ >= start_time)
    if end_time:
        base_query = base_query.filter(TaskInfo.CJSJ <= end_time)

    if ryid:
        assigned_tasks = db.query(TaskAssign.RWID, TaskAssign.FPSJ).filter(
            TaskAssign.RYID == ryid,
            TaskAssign.SFSC == 0
        ).order_by(TaskAssign.FPSJ.desc()).all()
        assigned_task_ids = [row[0] for row in assigned_tasks]
        if assigned_task_ids:
            base_query = base_query.filter(TaskInfo.ID.in_(assigned_task_ids))
            ordered_ids = list(dict.fromkeys(assigned_task_ids))
            case_stmt = case(*[(TaskInfo.ID == tid, idx) for idx, tid in enumerate(ordered_ids)], else_=len(ordered_ids))
            base_query = base_query.order_by(case_stmt)
        else:
            base_query = base_query.filter(TaskInfo.ID == -1)

    query = base_query
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()

    result = []
    for item in items:
        assignees = db.query(TaskAssign.RYID).filter(TaskAssign.RWID == item.ID, TaskAssign.SFSC == 0).distinct().all()
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
def get_task_stats(ryid: Optional[int] = Query(None), db: Session = Depends(get_db)):
    base_query = db.query(TaskInfo).filter(TaskInfo.SFSC == 0)
    if ryid:
        assigned_task_ids = db.query(TaskAssign.RWID).filter(
            TaskAssign.RYID == ryid,
            TaskAssign.SFSC == 0
        ).subquery()
        base_query = base_query.filter(TaskInfo.ID.in_(assigned_task_ids))

    total = base_query.count()
    draft = base_query.filter(TaskInfo.ZT == "draft").count()
    pending = base_query.filter(TaskInfo.ZT == "pending").count()
    processing = base_query.filter(TaskInfo.ZT == "processing").count()
    completed = base_query.filter(TaskInfo.ZT == "completed").count()

    return {"code": 200, "data": {"total": total, "draft": draft, "pending": pending, "processing": processing, "completed": completed}}


@router.post("", response_model=dict)
def create_task(data: TaskInfoCreate, db: Session = Depends(get_db)):
    for attempt in range(5):
        task_no = generate_task_number(db)

        ssql = data.SSQH
        if not ssql and data.plot_ids:
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
            ZT="draft"
        )
        db.add(db_item)
        try:
            db.commit()
            db.refresh(db_item)

            if data.plot_ids:
                for plot_id in data.plot_ids:
                    task_plot = TaskPlot(RWID=db_item.ID, DKID=plot_id)
                    db.add(task_plot)
                db.commit()

            return {"code": 200, "msg": "创建成功", "data": {"ID": db_item.ID, "RWBH": task_no}}
        except IntegrityError:
            db.rollback()
            db.expire_all()
            if attempt == 4:
                raise HTTPException(status_code=500, detail="任务编号生成失败，请重试")
            time.sleep(0.05 * (attempt + 1))


@router.post("/{task_id}/publish", response_model=dict)
def publish_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskInfo).filter(TaskInfo.ID == task_id, TaskInfo.SFSC == 0).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    if task.ZT != "draft":
        raise HTTPException(status_code=400, detail="只有待发布状态的任务才能发布")
    task.ZT = "pending"
    db.commit()
    return {"code": 200, "msg": "发布成功"}


@router.post("/{task_id}/plots/{plot_id}/assign", response_model=dict)
def assign_plot(task_id: int, plot_id: int, personnel_ids: List[int], db: Session = Depends(get_db)):
    task = db.query(TaskInfo).filter(TaskInfo.ID == task_id, TaskInfo.SFSC == 0).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    task_plot = db.query(TaskPlot).filter(TaskPlot.RWID == task_id, TaskPlot.DKID == plot_id, TaskPlot.SFSC == 0).first()
    if not task_plot:
        raise HTTPException(status_code=404, detail="地块不在该任务中")

    db.query(TaskAssign).filter(
        TaskAssign.RWID == task_id,
        TaskAssign.DKID == plot_id,
        TaskAssign.SFSC == 0
    ).update({"SFSC": 1})

    for person_id in personnel_ids:
        assign = TaskAssign(RWID=task_id, DKID=plot_id, RYID=person_id)
        db.add(assign)

    task.ZT = "processing"
    db.commit()
    return {"code": 200, "msg": "分配成功"}


@router.post("/{task_id}/assign", response_model=dict)
def assign_task(task_id: int, personnel_ids: List[int], db: Session = Depends(get_db)):
    task = db.query(TaskInfo).filter(TaskInfo.ID == task_id, TaskInfo.SFSC == 0).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    plots = db.query(TaskPlot).filter(TaskPlot.RWID == task_id, TaskPlot.SFSC == 0).all()
    for plot in plots:
        db.query(TaskAssign).filter(
            TaskAssign.RWID == task_id,
            TaskAssign.DKID == plot.DKID,
            TaskAssign.SFSC == 0
        ).update({"SFSC": 1})
        for person_id in personnel_ids:
            assign = TaskAssign(RWID=task_id, DKID=plot.DKID, RYID=person_id)
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
def get_task_detail(task_id: int, ryid: Optional[int] = Query(None, description="按用户过滤地块"), db: Session = Depends(get_db)):
    item = db.query(TaskInfo).filter(TaskInfo.ID == task_id, TaskInfo.SFSC == 0).first()
    if not item:
        raise HTTPException(status_code=404, detail="任务不存在")

    plots = db.query(TaskPlot).filter(TaskPlot.RWID == task_id, TaskPlot.SFSC == 0).all()
    plot_ids = [p.DKID for p in plots]

    if ryid:
        assigned_plot_ids = db.query(TaskAssign.DKID).filter(
            TaskAssign.RWID == task_id,
            TaskAssign.RYID == ryid,
            TaskAssign.SFSC == 0
        ).all()
        assigned_plot_ids = [row[0] for row in assigned_plot_ids]
        plots = [p for p in plots if p.DKID in assigned_plot_ids]
        plot_ids = assigned_plot_ids

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

    plot_assignments = {}
    for p in plot_objs:
        assigns = db.query(TaskAssign).filter(
            TaskAssign.RWID == task_id,
            TaskAssign.DKID == p.ID,
            TaskAssign.SFSC == 0
        ).all()
        plot_assignments[p.ID] = [a.RYID for a in assigns]

    contact = None
    if item.FZR:
        person = db.query(PersonInfo).filter(PersonInfo.XM == item.FZR, PersonInfo.SFSC == 0).first()
        if person and person.LXFS:
            from app.utils.crypto import decrypt_data
            contact = decrypt_data(person.LXFS)

    survey = db.query(SurveyRecord).filter(SurveyRecord.RWID == task_id, SurveyRecord.SFSC == 0).first()
    sample = db.query(SampleRecord).filter(SampleRecord.RWID == task_id, SampleRecord.SFSC == 0).first()

    earliest_survey_time = db.query(func.min(TaskPlotStatus.KCFSJ)).filter(
        TaskPlotStatus.RWID == task_id,
        TaskPlotStatus.KCFSJ.isnot(None),
        TaskPlotStatus.SFSC == 0
    ).scalar()

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
            "plot_assignments": plot_assignments,
            "survey_id": survey.ID if survey else None,
            "sample_id": sample.ID if sample else None,
            "actual_start_time": earliest_survey_time.strftime("%Y-%m-%d %H:%M:%S") if earliest_survey_time else None
        }
    }


UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads", "tasks")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_TYPES = {
    "application/pdf": ".pdf",
    "application/msword": ".doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.ms-excel": ".xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
}

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


@router.post("/{task_id}/attachments", response_model=dict)
async def upload_attachment(task_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    task = db.query(TaskInfo).filter(TaskInfo.ID == task_id, TaskInfo.SFSC == 0).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="不支持的文件类型")

    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超过50MB限制")

    ext = ALLOWED_TYPES[file.content_type]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as f:
        f.write(file_content)

    db_attachment = TaskAttachment(
        RWID=task_id,
        FILE_NAME=file.filename,
        FILE_PATH=file_path,
        FILE_SIZE=len(file_content),
        FILE_TYPE=file.content_type
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)

    return {"code": 200, "msg": "上传成功", "data": {"ID": db_attachment.ID, "FILE_NAME": db_attachment.FILE_NAME}}


@router.get("/{task_id}/attachments", response_model=dict)
def get_attachments(task_id: int, db: Session = Depends(get_db)):
    attachments = db.query(TaskAttachment).filter(
        TaskAttachment.RWID == task_id,
        TaskAttachment.SFSC == 0
    ).all()

    result = []
    for item in attachments:
        result.append({
            "ID": item.ID,
            "FILE_NAME": item.FILE_NAME,
            "FILE_SIZE": item.FILE_SIZE,
            "FILE_TYPE": item.FILE_TYPE,
            "CJSJ": item.CJSJ.strftime("%Y-%m-%d %H:%M:%S") if item.CJSJ else None
        })

    return {"code": 200, "data": result}


@router.delete("/attachments/{attachment_id}", response_model=dict)
def delete_attachment(attachment_id: int, db: Session = Depends(get_db)):
    attachment = db.query(TaskAttachment).filter(
        TaskAttachment.ID == attachment_id,
        TaskAttachment.SFSC == 0
    ).first()
    if not attachment:
        raise HTTPException(status_code=404, detail="附件不存在")

    if os.path.exists(attachment.FILE_PATH):
        os.remove(attachment.FILE_PATH)

    attachment.SFSC = 1
    db.commit()
    return {"code": 200, "msg": "删除成功"}


@router.get("/attachments/{attachment_id}/download")
def download_attachment(attachment_id: int, db: Session = Depends(get_db)):
    attachment = db.query(TaskAttachment).filter(
        TaskAttachment.ID == attachment_id,
        TaskAttachment.SFSC == 0
    ).first()
    if not attachment:
        raise HTTPException(status_code=404, detail="附件不存在")

    if not os.path.exists(attachment.FILE_PATH):
        raise HTTPException(status_code=404, detail="文件不存在")

    return FileResponse(
        attachment.FILE_PATH,
        media_type=attachment.FILE_TYPE,
        filename=attachment.FILE_NAME
    )
