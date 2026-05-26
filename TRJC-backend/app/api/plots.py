from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import PlotInfo, PersonInfo
from app.schemas.plot import PlotInfoCreate, PlotInfoUpdate, PlotInfoResponse, PlotOptionResponse
from app.utils.crypto import decrypt_data

router = APIRouter(prefix="/api/plots", tags=["地块管理"])


@router.get("", response_model=dict)
def get_plot_list(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    keyword: Optional[str] = None,
    ssqh: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(PlotInfo).filter(PlotInfo.SFSC == 0)

    if keyword:
        query = query.filter(PlotInfo.TBH.like(f"%{keyword}%"))
    if ssqh:
        query = query.filter(PlotInfo.SSQH == ssqh)

    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()

    result = []
    for item in items:
        result.append({
            "ID": item.ID,
            "TBH": item.TBH,
            "SSDY": item.SSDY,
            "TBMJ": float(item.TBMJ) if item.TBMJ else None,
            "SSQH": item.SSQH,
            "JD": float(item.JD) if item.JD else None,
            "WD": float(item.WD) if item.WD else None,
            "CJSJ": item.CJSJ
        })

    return {"code": 200, "data": {"list": result, "total": total, "page": page, "size": size}}


@router.get("/options", response_model=dict)
def get_plot_options(db: Session = Depends(get_db)):
    items = db.query(PlotInfo).filter(PlotInfo.SFSC == 0).all()
    result = [{"ID": item.ID, "TBH": item.TBH, "SSQH": item.SSQH, "TBMJ": float(item.TBMJ) if item.TBMJ else None} for item in items]
    return {"code": 200, "data": result}


@router.post("", response_model=dict)
def create_plot(data: PlotInfoCreate, request: Request, db: Session = Depends(get_db)):
    user_id = request.state.user_id
    db_item = PlotInfo(
        TBH=data.TBH,
        SSDY=data.SSDY,
        TBMJ=data.TBMJ,
        SSQH=data.SSQH,
        JD=data.JD,
        WD=data.WD,
        WLZB=data.WLZB,
        CJR=user_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"code": 200, "msg": "添加成功", "data": {"ID": db_item.ID}}


@router.put("/{plot_id}", response_model=dict)
def update_plot(plot_id: int, data: PlotInfoUpdate, db: Session = Depends(get_db)):
    item = db.query(PlotInfo).filter(PlotInfo.ID == plot_id, PlotInfo.SFSC == 0).first()
    if not item:
        raise HTTPException(status_code=404, detail="地块不存在")

    if data.TBH is not None:
        item.TBH = data.TBH
    if data.SSDY is not None:
        item.SSDY = data.SSDY
    if data.TBMJ is not None:
        item.TBMJ = data.TBMJ
    if data.SSQH is not None:
        item.SSQH = data.SSQH
    if data.JD is not None:
        item.JD = data.JD
    if data.WD is not None:
        item.WD = data.WD
    if data.WLZB is not None:
        item.WLZB = data.WLZB

    db.commit()
    return {"code": 200, "msg": "更新成功"}


@router.delete("/{plot_id}", response_model=dict)
def delete_plot(plot_id: int, db: Session = Depends(get_db)):
    item = db.query(PlotInfo).filter(PlotInfo.ID == plot_id, PlotInfo.SFSC == 0).first()
    if not item:
        raise HTTPException(status_code=404, detail="地块不存在")

    item.SFSC = 1
    db.commit()
    return {"code": 200, "msg": "删除成功"}


@router.get("/{plot_id}", response_model=dict)
def get_plot_detail(plot_id: int, db: Session = Depends(get_db)):
    item = db.query(PlotInfo).filter(PlotInfo.ID == plot_id, PlotInfo.SFSC == 0).first()
    if not item:
        raise HTTPException(status_code=404, detail="地块不存在")

    creator_name = ""
    if item.CJR:
        person = db.query(PersonInfo).filter(PersonInfo.ID == item.CJR, PersonInfo.SFSC == 0).first()
        if person:
            creator_name = decrypt_data(person.XM)

    return {
        "code": 200,
        "data": {
            "ID": item.ID,
            "TBH": item.TBH,
            "SSDY": item.SSDY,
            "TBMJ": float(item.TBMJ) if item.TBMJ else None,
            "SSQH": item.SSQH,
            "JD": float(item.JD) if item.JD else None,
            "WD": float(item.WD) if item.WD else None,
            "WLZB": item.WLZB,
            "CJSJ": item.CJSJ,
            "CJR": creator_name
        }
    }
