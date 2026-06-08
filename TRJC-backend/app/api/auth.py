from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel

from app.database import get_db
from app.models import PersonInfo
from app.utils.crypto import decrypt_data, hash_password, verify_password
from app.config import settings

try:
    from jose import jwt, JWTError
except ImportError:
    import jwt as _jwt
    jwt = _jwt
    JWTError = Exception

router = APIRouter(prefix="/api/auth", tags=["认证"])

security = HTTPBearer(auto_error=False)


@router.get("/companies", response_model=dict)
def get_companies(db: Session = Depends(get_db)):
    """获取所有不重复的公司列表（从人员表中提取）"""
    companies = db.query(PersonInfo.GS).filter(
        PersonInfo.SFSC == 0,
        PersonInfo.GS.isnot(None),
        PersonInfo.GS != ""
    ).distinct().all()
    result = sorted([c[0] for c in companies if c[0]])
    return {"code": 200, "data": result}


class LoginRequest(BaseModel):
    username: str
    password: str
    gs: str  # 所属公司


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(seconds=settings.JWT_EXPIRE_SECONDS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    if not credentials:
        raise HTTPException(status_code=401, detail="未提供认证信息")

    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="无效的认证令牌")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="无效的认证令牌")

    user = db.query(PersonInfo).filter(PersonInfo.ID == int(user_id), PersonInfo.SFSC == 0).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")

    return user


@router.post("/login", response_model=dict)
def login(login_data: LoginRequest, db: Session = Depends(get_db), request: Request = None):
    # 先根据公司过滤用户
    users = db.query(PersonInfo).filter(
        PersonInfo.SFSC == 0,
        PersonInfo.GS == login_data.gs
    ).all()

    user = None
    for u in users:
        try:
            decrypted_username = decrypt_data(u.YHM) if u.YHM else None
            decrypted_phone = decrypt_data(u.LXFS) if u.LXFS else None
            decrypted_name = decrypt_data(u.XM) if u.XM else None
            if (decrypted_username == login_data.username or
                decrypted_phone == login_data.username or
                decrypted_name == login_data.username):
                user = u
                break
        except Exception:
            continue

    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    if not user.MM:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    if not verify_password(login_data.password, user.MM):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    login_source = request.headers.get("X-Login-Source", "h5") if request else "h5"

    # 权限控制:
    # 管理员: 可登录Web+H5
    # 项目经理: 可登录Web+H5
    # 其他岗位: 仅可登录H5
    if login_source == "web" and user.GW not in ("管理员", "项目经理"):
        raise HTTPException(
            status_code=403,
            detail="该岗位不可登录Web端，请使用移动端登录"
        )

    token = create_access_token(data={"sub": str(user.ID), "gs": user.GS})

    return {
        "code": 200,
        "data": {
            "token": token,
            "expires_in": settings.JWT_EXPIRE_SECONDS,
            "user": {
                "ID": user.ID,
                "XM": decrypt_data(user.XM),
                "LXFS": decrypt_data(user.LXFS),
                "GW": user.GW,
                "SSQH": user.SSQH,
                "SSBM": user.SSBM,
                "GS": user.GS,
                "isAdmin": user.GW == "管理员"
            }
        }
    }


@router.post("/logout", response_model=dict)
def logout():
    return {"code": 200, "msg": "退出成功"}


@router.post("/refresh", response_model=dict)
def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    if not credentials:
        raise HTTPException(status_code=401, detail="未提供认证信息")

    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="无效的认证令牌")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="无效的认证令牌")

    new_token = create_access_token(data={"sub": str(user_id)})

    return {
        "code": 200,
        "data": {
            "token": new_token,
            "expires_in": settings.JWT_EXPIRE_SECONDS
        }
    }
