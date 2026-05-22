from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import SurveyRecord, TaskPlotStatus, TaskPlot, TaskInfo
from app.schemas.survey import SurveyRecordCreate, SurveyRecordUpdate, SurveyRecordResponse
from app.utils.task_helper import try_complete_task

router = APIRouter(prefix="/api/tasks/{task_id}/survey", tags=["勘察记录"])


@router.get("", response_model=dict)
def get_survey_records(task_id: int, db: Session = Depends(get_db)):
    items = db.query(SurveyRecord).filter(SurveyRecord.RWID == task_id, SurveyRecord.SFSC == 0).all()
    result = []
    for item in items:
        result.append({
            "ID": item.ID,
            "RWID": item.RWID,
            "DKID": item.DKID,
            "XMMC": item.XMMC,
            "TBH": item.TBH,
            "MJ": float(item.MJ) if item.MJ else None,
            "DLWZ": item.DLWZ,
            "DLZB_JD": item.DLZB_JD,
            "DLZB_WD": item.DLZB_WD,
            "BGQ": item.BGQ,
            "BGSJ": item.BGSJ,
            "LYLX": item.LYLX,
            "YXTCHD": float(item.YXTCHD) if item.YXTCHD else None,
            "QRLXJHL": item.QRLXJHL,
            "LSHL": float(item.LSHL) if item.LSHL else None,
            "DXPD": float(item.DXPD) if item.DXPD else None,
            "TMPZCD": item.TMPZCD,
            "SZBZTJ": item.SZBZTJ,
            "DLTXTJ": item.DLTXTJ,
            "DXBW": item.DXBW,
            "ZDGX": item.ZDGX,
            "PSNL": item.PSNL,
            "HBGD": float(item.HBGD) if item.HBGD else None,
            "NTFH": item.NTFH,
            "GCHD": float(item.GCHD) if item.GCHD else None,
            "KCRQ": item.KCRQ,
            "DCRY": item.DCRY,
            "XMDWDB": item.XMDWDB,
            "TKZJ": item.TKZJ
        })
    return {"code": 200, "data": result}


@router.post("", response_model=dict)
def create_survey_record(task_id: int, data: SurveyRecordCreate, db: Session = Depends(get_db)):
    db_item = SurveyRecord(
        RWID=data.RWID,
        DKID=data.DKID,
        XMMC=data.XMMC,
        TBH=data.TBH,
        MJ=data.MJ,
        DLWZ=data.DLWZ,
        DLZB_JD=data.DLZB_JD,
        DLZB_WD=data.DLZB_WD,
        BGQ=data.BGQ,
        BGSJ=data.BGSJ,
        LYLX=data.LYLX,
        YXTCHD=data.YXTCHD,
        QRLXJHL=data.QRLXJHL,
        LSHL=data.LSHL,
        DXPD=data.DXPD,
        TMPZCD=data.TMPZCD,
        SZBZTJ=data.SZBZTJ,
        DLTXTJ=data.DLTXTJ,
        DXBW=data.DXBW,
        ZDGX=data.ZDGX,
        PSNL=data.PSNL,
        HBGD=data.HBGD,
        NTFH=data.NTFH,
        GCHD=data.GCHD,
        KCRQ=data.KCRQ,
        DCRY=data.DCRY,
        XMDWDB=data.XMDWDB,
        TKZJ=data.TKZJ
    )
    db.add(db_item)
    
    status_record = db.query(TaskPlotStatus).filter(
        TaskPlotStatus.RWID == data.RWID,
        TaskPlotStatus.DKID == data.DKID,
        TaskPlotStatus.SFSC == 0
    ).first()
    
    if status_record:
        status_record.ZT = "transport"
        status_record.KCFSJ = datetime.now()
    else:
        status_record = TaskPlotStatus(
            RWID=data.RWID,
            DKID=data.DKID,
            ZT="transport",
            KCFSJ=datetime.now()
        )
        db.add(status_record)
    
    db.commit()
    try_complete_task(db, data.RWID)
    db.refresh(db_item)
    return {"code": 200, "msg": "提交成功", "data": {"ID": db_item.ID}}


@router.put("/{record_id}", response_model=dict)
def update_survey_record(task_id: int, record_id: int, data: SurveyRecordUpdate, db: Session = Depends(get_db)):
    item = db.query(SurveyRecord).filter(SurveyRecord.ID == record_id, SurveyRecord.SFSC == 0).first()
    if not item:
        raise HTTPException(status_code=404, detail="记录不存在")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    return {"code": 200, "msg": "更新成功"}
