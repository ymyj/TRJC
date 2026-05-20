from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PlotInfoBase(BaseModel):
    TBH: str
    SSDY: Optional[str] = None
    TBMJ: Optional[float] = None
    SSQH: Optional[str] = None
    JD: Optional[float] = None
    WD: Optional[float] = None
    WLZB: Optional[list] = None


class PlotInfoCreate(PlotInfoBase):
    pass


class PlotInfoUpdate(BaseModel):
    TBH: Optional[str] = None
    SSDY: Optional[str] = None
    TBMJ: Optional[float] = None
    SSQH: Optional[str] = None
    JD: Optional[float] = None
    WD: Optional[float] = None
    WLZB: Optional[list] = None


class PlotInfoResponse(BaseModel):
    ID: int
    TBH: str
    SSDY: Optional[str] = None
    TBMJ: Optional[float] = None
    SSQH: Optional[str] = None
    JD: Optional[float] = None
    WD: Optional[float] = None
    WLZB: Optional[list] = None
    CJSJ: Optional[datetime] = None
    SFSC: int = 0

    class Config:
        from_attributes = True


class PlotOptionResponse(BaseModel):
    ID: int
    TBH: str
    SSQH: Optional[str] = None
    TBMJ: Optional[float] = None

    class Config:
        from_attributes = True
