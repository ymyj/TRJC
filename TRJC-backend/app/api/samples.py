from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import SampleRecord
from app.schemas.sample import SampleRecordCreate, SampleRecordUpdate, SampleRecordResponse

router = APIRouter(prefix="/api/tasks/{task_id}/samples", tags=["样品采集"])


@router.get("", response_model=dict)
def get_sample_records(task_id: int, db: Session = Depends(get_db)):
    items = db.query(SampleRecord).filter(SampleRecord.RWID == task_id, SampleRecord.SFSC == 0).all()
    result = []
    for item in items:
        result.append({
            "ID": item.ID,
            "RWID": item.RWID,
            "DKID": item.DKID,
            "TRHHYPBH": item.TRHHYPBH,
            "DLWZ": item.DLWZ,
            "DLZB_D1BH": item.DLZB_D1BH,
            "DLZB_D1JD": item.DLZB_D1JD,
            "DLZB_D1WD": item.DLZB_D1WD,
            "DLZB_D2BH": item.DLZB_D2BH,
            "DLZB_D2JD": item.DLZB_D2JD,
            "DLZB_D2WD": item.DLZB_D2WD,
            "DLZB_D3BH": item.DLZB_D3BH,
            "DLZB_D3JD": item.DLZB_D3JD,
            "DLZB_D3WD": item.DLZB_D3WD,
            "CYSD_D1": item.CYSD_D1,
            "CYSD_D2": item.CYSD_D2,
            "CYSD_D3": item.CYSD_D3,
            "CYDWSL": item.CYDWSL,
            "HHYPSL": float(item.HHYPSL) if item.HHYPSL else None,
            "CYRQ": item.CYRQ,
            "CYRY": item.CYRY,
            "XMDWDB": item.XMDWDB,
            "TKZJ": item.TKZJ
        })
    return {"code": 200, "data": result}


@router.post("", response_model=dict)
def create_sample_record(task_id: int, data: SampleRecordCreate, db: Session = Depends(get_db)):
    db_item = SampleRecord(
        RWID=data.RWID,
        DKID=data.DKID,
        TRHHYPBH=data.TRHHYPBH,
        DLWZ=data.DLWZ,
        DLZB_D1BH=data.DLZB_D1BH,
        DLZB_D1JD=data.DLZB_D1JD,
        DLZB_D1WD=data.DLZB_D1WD,
        DLZB_D2BH=data.DLZB_D2BH,
        DLZB_D2JD=data.DLZB_D2JD,
        DLZB_D2WD=data.DLZB_D2WD,
        DLZB_D3BH=data.DLZB_D3BH,
        DLZB_D3JD=data.DLZB_D3JD,
        DLZB_D3WD=data.DLZB_D3WD,
        CYSD_D1=data.CYSD_D1,
        CYSD_D2=data.CYSD_D2,
        CYSD_D3=data.CYSD_D3,
        CYDWSL=data.CYDWSL,
        HHYPSL=data.HHYPSL,
        CYRQ=data.CYRQ,
        CYRY=data.CYRY,
        XMDWDB=data.XMDWDB,
        TKZJ=data.TKZJ
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"code": 200, "msg": "提交成功", "data": {"ID": db_item.ID}}


@router.put("/{record_id}", response_model=dict)
def update_sample_record(task_id: int, record_id: int, data: SampleRecordUpdate, db: Session = Depends(get_db)):
    item = db.query(SampleRecord).filter(SampleRecord.ID == record_id, SampleRecord.SFSC == 0).first()
    if not item:
        raise HTTPException(status_code=404, detail="记录不存在")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    return {"code": 200, "msg": "更新成功"}
