from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class PersonInfoBase(BaseModel):
    YHM: Optional[str] = None
    XM: str
    LXFS: str
    password: Optional[str] = None
    GW: str
    SSQH: Optional[str] = None
    SSBM: Optional[str] = None
    RYZT: str = "active"


class PersonInfoCreate(PersonInfoBase):
    pass


class PersonInfoUpdate(BaseModel):
    YHM: Optional[str] = None
    XM: Optional[str] = None
    LXFS: Optional[str] = None
    password: Optional[str] = None
    GW: Optional[str] = None
    SSQH: Optional[str] = None
    SSBM: Optional[str] = None
    RYZT: Optional[str] = None


class PersonInfoResponse(BaseModel):
    ID: int
    XM: str
    LXFS: str
    GW: str
    SSQH: Optional[str] = None
    SSBM: Optional[str] = None
    RYZT: str
    CJSJ: Optional[datetime] = None
    SFSC: int = 0

    class Config:
        from_attributes = True


class PersonInfoListResponse(BaseModel):
    ID: int
    XM: str
    LXFS: str
    GW: str
    SSQH: Optional[str] = None
    SSBM: Optional[str] = None
    RYZT: str
    CJSJ: Optional[datetime] = None

    class Config:
        from_attributes = True
