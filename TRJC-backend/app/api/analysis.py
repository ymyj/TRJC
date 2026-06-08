from fastapi import APIRouter, Depends, HTTPException, Request
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
    
    try:
        from app.utils.dataset_helper import _create_dataset_from_completed_plot
        _create_dataset_from_completed_plot(db, data.RWID, data.DKID)
        db.commit()
    except Exception as e:
        print(f"自动创建数据集记录失败: {e}")
    
    db.refresh(db_item)
    return {"code": 200, "msg": "提交成功", "data": {"ID": db_item.ID}}


@router.post("/batch", response_model=dict)
async def create_analysis_result_batch(task_id: int, request: Request, db: Session = Depends(get_db)):
    """批量提交分析结果：勾选多个地块，填写一份分析数据，所有地块共享相同的分析结果"""
    import json
    raw_body = await request.body()
    print(f"[DEBUG] Batch analysis raw body: {raw_body}")
    
    try:
        data = json.loads(raw_body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"JSON解析失败: {str(e)}")
    
    common = data.get('common', {})
    plot_ids = data.get('plotIds', [])
    
    if not plot_ids:
        raise HTTPException(status_code=400, detail="请选择至少一个地块")
    
    try:
        # 批量提交前先清理该任务下已有的分析记录
        existing_records = db.query(AnalysisResult).filter(
            AnalysisResult.RWID == task_id,
            AnalysisResult.SFSC == 0
        ).all()
        for rec in existing_records:
            rec.SFSC = 1
        db.flush()
        
        for dkid in plot_ids:
            db_item = AnalysisResult(
                RWID=task_id,
                DKID=dkid,
                RZ=common.get('RZ'),
                PHZ=common.get('PHZ'),
                YJZ=common.get('YJZ'),
                YXP=common.get('YXP'),
                XJK=common.get('XJK'),
                SRXYLZL=common.get('SRXYLZL'),
                GE=common.get('GE'),
                ZG=common.get('ZG'),
                ZS=common.get('ZS'),
                QIAN=common.get('QIAN'),
                GE_CHROME=common.get('GE_CHROME')
            )
            db.add(db_item)
            
            status_record = db.query(TaskPlotStatus).filter(
                TaskPlotStatus.RWID == task_id,
                TaskPlotStatus.DKID == dkid,
                TaskPlotStatus.SFSC == 0
            ).first()
            
            if status_record:
                status_record.ZT = "completed"
                status_record.CYFSJ = datetime.now()
            else:
                status_record = TaskPlotStatus(
                    RWID=task_id,
                    DKID=dkid,
                    ZT="completed",
                    CYFSJ=datetime.now()
                )
                db.add(status_record)
            
            try:
                from app.utils.dataset_helper import _create_dataset_from_completed_plot
                _create_dataset_from_completed_plot(db, task_id, dkid, preloaded_analysis=common)
            except Exception as e:
                print(f"地块{dkid}创建数据集记录失败: {e}")
        
        db.commit()
        try_complete_task(db, task_id)
        
        return {"code": 200, "msg": f"批量分析提交成功，共{len(plot_ids)}个地块", "data": {"count": len(plot_ids)}}
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Batch analysis submit failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"批量分析提交失败: {str(e)}")
