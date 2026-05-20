from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import FarmlandDataset
from app.schemas.dataset import FarmlandDatasetCreate, FarmlandDatasetUpdate, FarmlandDatasetResponse

router = APIRouter(prefix="/api/datasets", tags=["耕地质量数据集"])


@router.get("", response_model=dict)
def get_dataset_list(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(FarmlandDataset).filter(FarmlandDataset.SFSC == 0)

    if keyword:
        query = query.filter(FarmlandDataset.RWMC.like(f"%{keyword}%"))

    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()

    result = []
    for item in items:
        result.append({
            "ID": item.ID,
            "RWMC": item.RWMC,
            "TBH": item.TBH,
            "JD": float(item.JD) if item.JD else None,
            "WD": float(item.WD) if item.WD else None,
            "GDZLDJ": float(item.GDZLDJ) if item.GDZLDJ else None,
            "ZLFJ": item.ZLFJ,
            "CYRQ": item.CYRQ
        })

    return {"code": 200, "data": {"list": result, "total": total, "page": page, "size": size}}


@router.post("", response_model=dict)
def create_dataset(data: FarmlandDatasetCreate, db: Session = Depends(get_db)):
    db_item = FarmlandDataset(
        RWID=data.RWID,
        DKID=data.DKID,
        RWMC=data.RWMC,
        TBH=data.TBH,
        JD=data.JD,
        WD=data.WD,
        CYRQ=data.CYRQ,
        DXBW=data.DXBW,
        YXTCHD=data.YXTCHD,
        GCZD=data.GCZD,
        RZ=data.RZ,
        ZDGX=data.ZDGX,
        SWDYX=data.SWDYX,
        NTLW=data.NTLW,
        ZAYS=data.ZAYS,
        GGNL=data.GGNL,
        PSNL=data.PSNL,
        PHZ=data.PHZ,
        YJZ=data.YJZ,
        YXL=data.YXL,
        SXJ=data.SXJ,
        SRXYLZL=data.SRXYLZL,
        DLMC=data.DLMC,
        JQCD=data.JQCD,
        BZ=data.BZ,
        GD=data.GD,
        ZG=data.ZG,
        ZS=data.ZS,
        Q=data.Q,
        G=data.G,
        GDZLDJ=data.GDZLDJ,
        ZLFJ=data.ZLFJ
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"code": 200, "msg": "创建成功", "data": {"ID": db_item.ID}}


@router.get("/{dataset_id}", response_model=dict)
def get_dataset_detail(dataset_id: int, db: Session = Depends(get_db)):
    item = db.query(FarmlandDataset).filter(FarmlandDataset.ID == dataset_id, FarmlandDataset.SFSC == 0).first()
    if not item:
        raise HTTPException(status_code=404, detail="数据集不存在")

    return {
        "code": 200,
        "data": {
            "ID": item.ID,
            "RWID": item.RWID,
            "DKID": item.DKID,
            "RWMC": item.RWMC,
            "TBH": item.TBH,
            "JD": float(item.JD) if item.JD else None,
            "WD": float(item.WD) if item.WD else None,
            "CYRQ": item.CYRQ,
            "DXBW": item.DXBW,
            "YXTCHD": float(item.YXTCHD) if item.YXTCHD else None,
            "GCZD": item.GCZD,
            "RZ": float(item.RZ) if item.RZ else None,
            "ZDGX": item.ZDGX,
            "SWDYX": item.SWDYX,
            "NTLW": item.NTLW,
            "ZAYS": item.ZAYS,
            "GGNL": item.GGNL,
            "PSNL": item.PSNL,
            "PHZ": float(item.PHZ) if item.PHZ else None,
            "YJZ": float(item.YJZ) if item.YJZ else None,
            "YXL": float(item.YXL) if item.YXL else None,
            "SXJ": float(item.SXJ) if item.SXJ else None,
            "SRXYLZL": float(item.SRXYLZL) if item.SRXYLZL else None,
            "DLMC": item.DLMC,
            "JQCD": item.JQCD,
            "BZ": item.BZ,
            "GD": float(item.GD) if item.GD else None,
            "ZG": float(item.ZG) if item.ZG else None,
            "ZS": float(item.ZS) if item.ZS else None,
            "Q": float(item.Q) if item.Q else None,
            "G": float(item.G) if item.G else None,
            "GDZLDJ": float(item.GDZLDJ) if item.GDZLDJ else None,
            "ZLFJ": item.ZLFJ
        }
    }
