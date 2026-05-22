from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import SampleRecord, TaskPlotStatus, TaskPlot, TaskInfo
from app.schemas.sample import SampleRecordCreate, SampleRecordUpdate, SampleRecordResponse
import json
from app.utils.task_helper import try_complete_task

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
async def create_sample_record(task_id: int, request: Request, db: Session = Depends(get_db)):
    raw_body = await request.body()
    print(f"[DEBUG] Raw request body: {raw_body}")
    
    try:
        data_dict = json.loads(raw_body)
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    print(f"[DEBUG] Parsed data: {json.dumps(data_dict, ensure_ascii=False, indent=2)}")
    
    cyrq_date = None
    if data_dict.get('CYRQ'):
        try:
            cyrq_date = datetime.strptime(str(data_dict['CYRQ']), "%Y-%m-%d").date()
        except ValueError:
            pass

    cydwsl = None
    if data_dict.get('CYDWSL'):
        try:
            cydwsl = int(data_dict['CYDWSL'])
        except ValueError:
            pass

    hhypsl = None
    if data_dict.get('HHYPSL'):
        try:
            hhypsl = float(data_dict['HHYPSL'])
        except ValueError:
            pass

    db_item = SampleRecord(
        RWID=data_dict.get('RWID'),
        DKID=data_dict.get('DKID'),
        TRHHYPBH=data_dict.get('TRHHYPBH'),
        DLWZ=data_dict.get('DLWZ'),
        DLZB_D1BH=data_dict.get('DLZB_D1BH', ''),
        DLZB_D1JD=data_dict.get('DLZB_D1JD', ''),
        DLZB_D1WD=data_dict.get('DLZB_D1WD', ''),
        DLZB_D2BH=data_dict.get('DLZB_D2BH'),
        DLZB_D2JD=data_dict.get('DLZB_D2JD'),
        DLZB_D2WD=data_dict.get('DLZB_D2WD'),
        DLZB_D3BH=data_dict.get('DLZB_D3BH'),
        DLZB_D3JD=data_dict.get('DLZB_D3JD'),
        DLZB_D3WD=data_dict.get('DLZB_D3WD'),
        CYSD_D1=data_dict.get('CYSD_D1'),
        CYSD_D2=data_dict.get('CYSD_D2'),
        CYSD_D3=data_dict.get('CYSD_D3'),
        CYDWSL=cydwsl,
        HHYPSL=hhypsl,
        CYRQ=cyrq_date,
        CYRY=data_dict.get('CYRY'),
        XMDWDB=data_dict.get('XMDWDB'),
        TKZJ=data_dict.get('TKZJ')
    )
    db.add(db_item)
    
    rwid = data_dict.get('RWID')
    dkid = data_dict.get('DKID')
    status_record = db.query(TaskPlotStatus).filter(
        TaskPlotStatus.RWID == rwid,
        TaskPlotStatus.DKID == dkid,
        TaskPlotStatus.SFSC == 0
    ).first()
    
    if status_record:
        status_record.ZT = "analysis"
        status_record.CYFSJ = datetime.now()
    else:
        status_record = TaskPlotStatus(
            RWID=rwid,
            DKID=dkid,
            ZT="analysis",
            CYFSJ=datetime.now()
        )
        db.add(status_record)
    
    db.commit()
    try_complete_task(db, rwid)
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
