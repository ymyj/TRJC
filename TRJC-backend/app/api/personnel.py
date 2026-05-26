from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import PersonInfo
from app.schemas.personnel import PersonInfoCreate, PersonInfoUpdate, PersonInfoResponse, PersonInfoListResponse
from app.utils.crypto import encrypt_data, decrypt_data, mask_name, mask_phone

router = APIRouter(prefix="/api/personnel", tags=["人员管理"])


@router.get("", response_model=dict)
def get_personnel_list(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    keyword: Optional[str] = None,
    gw: Optional[str] = None,
    ssqh: Optional[str] = None,
    ryzt: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(PersonInfo).filter(PersonInfo.SFSC == 0)

    if gw:
        query = query.filter(PersonInfo.GW == gw)
    if ssqh:
        query = query.filter(PersonInfo.SSQH == ssqh)
    if ryzt:
        query = query.filter(PersonInfo.RYZT == ryzt)

    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()

    if keyword:
        items = [item for item in items if keyword in decrypt_data(item.XM)]
        total = len(items)

    result = []
    for item in items:
        item_dict = {
            "ID": item.ID,
            "XM": mask_name(decrypt_data(item.XM)),
            "LXFS": mask_phone(decrypt_data(item.LXFS)),
            "GW": item.GW,
            "SSQH": item.SSQH,
            "SSBM": item.SSBM,
            "RYZT": item.RYZT,
            "CJSJ": item.CJSJ
        }
        result.append(item_dict)

    return {"code": 200, "data": {"list": result, "total": total, "page": page, "size": size}}


@router.get("/options", response_model=dict)
def get_personnel_options(db: Session = Depends(get_db)):
    items = db.query(PersonInfo).filter(PersonInfo.SFSC == 0, PersonInfo.RYZT == "active").all()
    result = [{"ID": item.ID, "XM": decrypt_data(item.XM), "GW": item.GW, "SSQH": item.SSQH} for item in items]
    return {"code": 200, "data": result}


@router.get("/for-assignment", response_model=dict)
def get_personnel_for_assignment(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(PersonInfo).filter(PersonInfo.SFSC == 0, PersonInfo.RYZT == "active")

    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()

    result = []
    for item in items:
        item_dict = {
            "ID": item.ID,
            "XM": decrypt_data(item.XM),
            "LXFS": decrypt_data(item.LXFS),
            "GW": item.GW,
            "SSQH": item.SSQH,
            "SSBM": item.SSBM
        }
        result.append(item_dict)

    return {"code": 200, "data": {"list": result, "total": total, "page": page, "size": size}}


@router.post("", response_model=dict)
def create_personnel(data: PersonInfoCreate, db: Session = Depends(get_db)):
    db_item = PersonInfo(
        XM=encrypt_data(data.XM),
        LXFS=encrypt_data(data.LXFS),
        GW=data.GW,
        SSQH=data.SSQH,
        SSBM=data.SSBM,
        RYZT=data.RYZT
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"code": 200, "msg": "添加成功", "data": {"ID": db_item.ID}}


@router.put("/{person_id}", response_model=dict)
def update_personnel(person_id: int, data: PersonInfoUpdate, db: Session = Depends(get_db)):
    item = db.query(PersonInfo).filter(PersonInfo.ID == person_id, PersonInfo.SFSC == 0).first()
    if not item:
        raise HTTPException(status_code=404, detail="人员不存在")

    if data.XM is not None:
        item.XM = encrypt_data(data.XM)
    if data.LXFS is not None:
        item.LXFS = encrypt_data(data.LXFS)
    if data.GW is not None:
        item.GW = data.GW
    if data.SSQH is not None:
        item.SSQH = data.SSQH
    if data.SSBM is not None:
        item.SSBM = data.SSBM
    if data.RYZT is not None:
        item.RYZT = data.RYZT

    db.commit()
    return {"code": 200, "msg": "更新成功"}


@router.delete("/{person_id}", response_model=dict)
def delete_personnel(person_id: int, db: Session = Depends(get_db)):
    item = db.query(PersonInfo).filter(PersonInfo.ID == person_id, PersonInfo.SFSC == 0).first()
    if not item:
        raise HTTPException(status_code=404, detail="人员不存在")

    item.SFSC = 1
    db.commit()
    return {"code": 200, "msg": "删除成功"}


@router.get("/{person_id}", response_model=dict)
def get_personnel_detail(person_id: int, db: Session = Depends(get_db)):
    item = db.query(PersonInfo).filter(PersonInfo.ID == person_id, PersonInfo.SFSC == 0).first()
    if not item:
        raise HTTPException(status_code=404, detail="人员不存在")

    return {
        "code": 200,
        "data": {
            "ID": item.ID,
            "XM": decrypt_data(item.XM),
            "LXFS": decrypt_data(item.LXFS),
            "GW": item.GW,
            "SSQH": item.SSQH,
            "SSBM": item.SSBM,
            "RYZT": item.RYZT,
            "CJSJ": item.CJSJ
        }
    }
