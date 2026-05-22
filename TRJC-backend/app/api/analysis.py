from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import AnalysisResult, TaskPlotStatus
from app.schemas.analysis import AnalysisResultCreate, AnalysisResultUpdate, AnalysisResultResponse
from app.utils.task_helper import try_complete_task

router = APIRouter(prefix="/api/tasks/{task_id}/analysis", tags=["分析结果"])


@router.get("", response_model=dict)
def get_analysis_results(task_id: int, db: Session = Depends(get_db)):
    items = db.query(AnalysisResult).filter(AnalysisResult.RWID == task_id, AnalysisResult.SFSC == 0).all()
    result = []
    for item in items:
        result.append({
            "ID": item.ID,
            "RWID": item.RWID,
            "DKID": item.DKID,
            "RZ": float(item.RZ) if item.RZ else None,
            "PHZ": float(item.PHZ) if item.PHZ else None,
            "YJZ": float(item.YJZ) if item.YJZ else None,
            "YXP": float(item.YXP) if item.YXP else None,
            "XJK": float(item.XJK) if item.XJK else None,
            "SRXYLZL": float(item.SRXYLZL) if item.SRXYLZL else None,
            "GE": float(item.GE) if item.GE else None,
            "ZG": float(item.ZG) if item.ZG else None,
            "ZS": float(item.ZS) if item.ZS else None,
            "QIAN": float(item.QIAN) if item.QIAN else None,
            "GE_CHROME": float(item.GE_CHROME) if item.GE_CHROME else None,
        })
    return {"code": 200, "data": result}


@router.post("", response_model=dict)
def create_analysis_result(task_id: int, data: AnalysisResultCreate, db: Session = Depends(get_db)):
    db_item = AnalysisResult(
        RWID=data.RWID,
        DKID=data.DKID,
        RZ=data.RZ,
        PHZ=data.PHZ,
        YJZ=data.YJZ,
        YXP=data.YXP,
        XJK=data.XJK,
        SRXYLZL=data.SRXYLZL,
        GE=data.GE,
        ZG=data.ZG,
        ZS=data.ZS,
        QIAN=data.QIAN,
        GE_CHROME=data.GE_CHROME
    )
    db.add(db_item)
    
    status_record = db.query(TaskPlotStatus).filter(
        TaskPlotStatus.RWID == data.RWID,
        TaskPlotStatus.DKID == data.DKID,
        TaskPlotStatus.SFSC == 0
    ).first()
    
    if status_record:
        status_record.ZT = "completed"
        status_record.CYFSJ = datetime.now()
    else:
        status_record = TaskPlotStatus(
            RWID=data.RWID,
            DKID=data.DKID,
            ZT="completed",
            CYFSJ=datetime.now()
        )
        db.add(status_record)
    
    db.commit()
    
    from app.utils.task_helper import try_complete_task
    try_complete_task(db, data.RWID)
    
    db.refresh(db_item)
    return {"code": 200, "msg": "提交成功", "data": {"ID": db_item.ID}}


@router.put("/{record_id}", response_model=dict)
def update_analysis_result(task_id: int, record_id: int, data: AnalysisResultUpdate, db: Session = Depends(get_db)):
    item = db.query(AnalysisResult).filter(AnalysisResult.ID == record_id, AnalysisResult.SFSC == 0).first()
    if not item:
        raise HTTPException(status_code=404, detail="记录不存在")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    return {"code": 200, "msg": "更新成功"}
