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


@router.post("/batch", response_model=dict)
async def create_sample_records_batch(task_id: int, request: Request, db: Session = Depends(get_db)):
    raw_body = await request.body()
    print(f"[DEBUG] Batch raw request body: {raw_body}")
    
    try:
        data_dict = json.loads(raw_body)
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    print(f"[DEBUG] Batch parsed data: {json.dumps(data_dict, ensure_ascii=False, indent=2)}")
    
    common = data_dict.get('common', {})
    plots = data_dict.get('plots', [])
    
    if not plots:
        raise HTTPException(status_code=400, detail="至少选择一个地块")
    
    cyrq_date = None
    if common.get('CYRQ'):
        try:
            cyrq_date = datetime.strptime(str(common['CYRQ']), "%Y-%m-%d").date()
        except ValueError:
            pass

    cydwsl = None
    if common.get('CYDWSL'):
        try:
            cydwsl = int(common['CYDWSL'])
        except ValueError:
            pass

    hhypsl = None
    if common.get('HHYPSL'):
        try:
            hhypsl = float(common['HHYPSL'])
        except ValueError:
            pass

    created_items = []
    try:
        # 批量提交前先清理该任务下已有的采样记录（避免重复数据）
        existing_records = db.query(SampleRecord).filter(
            SampleRecord.RWID == task_id,
            SampleRecord.SFSC == 0
        ).all()
        for rec in existing_records:
            rec.SFSC = 1
        db.flush()
        
        for plot_data in plots:
            dkid = plot_data.get('DKID')
            
            dlzb_d1bh = plot_data.get('DLZB_D1BH', '')
            dlzb_d1jd = plot_data.get('DLZB_D1JD', '')
            dlzb_d1wd = plot_data.get('DLZB_D1WD', '')
            dlzb_d2bh = plot_data.get('DLZB_D2BH')
            dlzb_d2jd = plot_data.get('DLZB_D2JD')
            dlzb_d2wd = plot_data.get('DLZB_D2WD')
            dlzb_d3bh = plot_data.get('DLZB_D3BH')
            dlzb_d3jd = plot_data.get('DLZB_D3JD')
            dlzb_d3wd = plot_data.get('DLZB_D3WD')
            cysd_d1 = plot_data.get('CYSD_D1')
            cysd_d2 = plot_data.get('CYSD_D2')
            cysd_d3 = plot_data.get('CYSD_D3')
            
            db_item = SampleRecord(
                RWID=task_id,
                DKID=dkid,
                TRHHYPBH=common.get('TRHHYPBH'),
                DLWZ=common.get('DLWZ'),
                DLZB_D1BH=dlzb_d1bh,
                DLZB_D1JD=dlzb_d1jd,
                DLZB_D1WD=dlzb_d1wd,
                DLZB_D2BH=dlzb_d2bh,
                DLZB_D2JD=dlzb_d2jd,
                DLZB_D2WD=dlzb_d2wd,
                DLZB_D3BH=dlzb_d3bh,
                DLZB_D3JD=dlzb_d3jd,
                DLZB_D3WD=dlzb_d3wd,
                CYSD_D1=cysd_d1,
                CYSD_D2=cysd_d2,
                CYSD_D3=cysd_d3,
                CYDWSL=cydwsl,
                HHYPSL=hhypsl,
                CYRQ=cyrq_date,
                CYRY=common.get('CYRY'),
                XMDWDB=common.get('XMDWDB'),
                TKZJ=common.get('TKZJ')
            )
            db.add(db_item)
            created_items.append(db_item)
            
            status_record = db.query(TaskPlotStatus).filter(
                TaskPlotStatus.RWID == task_id,
                TaskPlotStatus.DKID == dkid,
                TaskPlotStatus.SFSC == 0
            ).first()
            
            if status_record:
                status_record.ZT = "analysis"
                status_record.CYFSJ = datetime.now()
            else:
                status_record = TaskPlotStatus(
                    RWID=task_id,
                    DKID=dkid,
                    ZT="analysis",
                    CYFSJ=datetime.now()
                )
                db.add(status_record)
        
        db.commit()
        
        for item in created_items:
            db.refresh(item)
        
        created_ids = [item.ID for item in created_items]
        try_complete_task(db, task_id)
        
        return {"code": 200, "msg": f"批量提交成功，共{len(plots)}个地块", "data": {"count": len(plots), "ids": created_ids}}
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Batch submit failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"批量提交失败: {str(e)}")


@router.put("/{record_id}", response_model=dict)
def update_sample_record(task_id: int, record_id: int, data: SampleRecordUpdate, db: Session = Depends(get_db)):
    item = db.query(SampleRecord).filter(SampleRecord.ID == record_id, SampleRecord.SFSC == 0).first()
    if not item:
        raise HTTPException(status_code=404, detail="记录不存在")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    return {"code": 200, "msg": "更新成功"}
