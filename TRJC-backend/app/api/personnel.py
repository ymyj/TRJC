from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import PersonInfo
from app.schemas.personnel import PersonInfoCreate, PersonInfoUpdate, PersonInfoResponse, PersonInfoListResponse
from app.utils.crypto import encrypt_data, decrypt_data, mask_phone, hash_password
from app.api.auth import get_current_user, is_super_admin, is_company_admin

router = APIRouter(prefix="/api/personnel", tags=["人员管理"])


@router.get("", response_model=dict)
def get_personnel_list(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    keyword: Optional[str] = None,
    gw: Optional[str] = None,
    ssqh: Optional[str] = None,
    gs: Optional[str] = None,
    ryzt: Optional[str] = None,
    current_user: PersonInfo = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(PersonInfo).filter(
        PersonInfo.SFSC == 0,
        PersonInfo.GW != "超管"  # 过滤掉超管账号，不显示在列表中
    ).order_by(PersonInfo.CJSJ.desc())

    # 权限控制：根据当前用户角色过滤
    if is_super_admin(current_user):
        # 超管：可查看所有人员，支持按公司筛选
        if gs:
            query = query.filter(PersonInfo.GS.like(f"%{gs}%"))
    elif is_company_admin(current_user):
        # 企业管理员：只能看本公司的人员
        query = query.filter(PersonInfo.GS == current_user.GS)
    else:
        # 其他岗位：只能看本公司人员
        if current_user.GS:
            query = query.filter(PersonInfo.GS == current_user.GS)

    if keyword:
        query = query.filter(PersonInfo.XM.contains(keyword))

    if gw:
        query = query.filter(PersonInfo.GW == gw)
    if ssqh:
        query = query.filter(PersonInfo.SSQH == ssqh)
    if gs:
        query = query.filter(PersonInfo.GS == gs)
    if ryzt:
        query = query.filter(PersonInfo.RYZT == ryzt)

    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()

    result = []
    for item in items:
        item_dict = {
            "ID": item.ID,
            "XM": item.XM,
            "LXFS": mask_phone(decrypt_data(item.LXFS)),
            "GW": item.GW,
            "SSQH": item.SSQH,
            "SSBM": item.SSBM,
            "GS": item.GS,
            "RYZT": item.RYZT,
            "CJSJ": item.CJSJ.strftime("%Y-%m-%d %H:%M:%S") if item.CJSJ else None
        }
        result.append(item_dict)

    return {"code": 200, "data": {"list": result, "total": total, "page": page, "size": size}}


@router.get("/options", response_model=dict)
def get_personnel_options(db: Session = Depends(get_db)):
    items = db.query(PersonInfo).filter(PersonInfo.SFSC == 0, PersonInfo.RYZT == "active").all()
    result = [{"ID": item.ID, "XM": item.XM, "GW": item.GW, "SSQH": item.SSQH, "GS": item.GS} for item in items]
    return {"code": 200, "data": result}


@router.get("/for-assignment", response_model=dict)
def get_personnel_for_assignment(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_user: PersonInfo = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(PersonInfo).filter(PersonInfo.SFSC == 0, PersonInfo.RYZT == "active")

    # 权限控制：根据当前用户角色过滤
    if is_company_admin(current_user):
        # 企业管理员：只能看本公司的人员
        query = query.filter(PersonInfo.GS == current_user.GS)
    elif current_user.GS:
        # 其他岗位：只能看本公司人员
        query = query.filter(PersonInfo.GS == current_user.GS)
    # 超管：查看所有人员，不做过滤

    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()

    result = []
    for item in items:
        item_dict = {
            "ID": item.ID,
            "XM": item.XM,
            "LXFS": decrypt_data(item.LXFS),
            "GW": item.GW,
            "SSQH": item.SSQH,
            "SSBM": item.SSBM,
            "GS": item.GS
        }
        result.append(item_dict)

    return {"code": 200, "data": {"list": result, "total": total, "page": page, "size": size}}


@router.post("", response_model=dict)
def create_personnel(
    data: PersonInfoCreate,
    current_user: PersonInfo = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 权限控制：企业管理员添加子账号时，强制使用本公司
    if is_super_admin(current_user):
        # 超管：可指定任意公司
        final_gs = data.GS
    else:
        # 非超管：强制使用当前用户所属公司
        final_gs = current_user.GS

    db_item = PersonInfo(
        XM=data.XM,
        LXFS=encrypt_data(data.LXFS),
        MM=hash_password(data.password) if data.password else None,
        GW=data.GW,
        SSQH=data.SSQH,
        SSBM=data.SSBM,
        GS=final_gs,
        RYZT=data.RYZT
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"code": 200, "msg": "添加成功", "data": {"ID": db_item.ID}}


@router.put("/{person_id}", response_model=dict)
def update_personnel(
    person_id: int,
    data: PersonInfoUpdate,
    current_user: PersonInfo = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(PersonInfo).filter(PersonInfo.ID == person_id, PersonInfo.SFSC == 0).first()
    if not item:
        raise HTTPException(status_code=404, detail="人员不存在")

    # 非超管不能修改公司字段
    if not is_super_admin(current_user):
        data.GS = None  # 忽略公司字段修改

    if data.XM is not None:
        item.XM = data.XM
    if data.LXFS is not None:
        item.LXFS = encrypt_data(data.LXFS)
    if data.password is not None:
        item.MM = hash_password(data.password)
    if data.GW is not None:
        item.GW = data.GW
    if data.SSQH is not None:
        item.SSQH = data.SSQH
    if data.SSBM is not None:
        item.SSBM = data.SSBM
    if data.GS is not None:
        item.GS = data.GS
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
            "XM": item.XM,
            "LXFS": decrypt_data(item.LXFS),
            "GW": item.GW,
            "SSQH": item.SSQH,
            "SSBM": item.SSBM,
            "GS": item.GS,
            "RYZT": item.RYZT,
            "CJSJ": item.CJSJ.strftime("%Y-%m-%d %H:%M:%S") if item.CJSJ else None
        }
    }
