from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class PersonInfoBase(BaseModel):
    XM: str
    LXFS: str
    GW: str
    SSQH: Optional[str] = None
    SSBM: Optional[str] = None
    RYZT: str = "active"


class PersonInfoCreate(PersonInfoBase):
    pass


class PersonInfoUpdate(BaseModel):
    XM: Optional[str] = None
    LXFS: Optional[str] = None
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
