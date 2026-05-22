from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class AnalysisResultBase(BaseModel):
    RWID: int
    DKID: int
    RZ: Optional[float] = None
    PHZ: Optional[float] = None
    YJZ: Optional[float] = None
    YXP: Optional[float] = None
    XJK: Optional[float] = None
    SRXYLZL: Optional[float] = None
    GE: Optional[float] = None
    ZG: Optional[float] = None
    ZS: Optional[float] = None
    QIAN: Optional[float] = None
    GE_CHROME: Optional[float] = None


class AnalysisResultCreate(AnalysisResultBase):
    pass


class AnalysisResultUpdate(BaseModel):
    RZ: Optional[float] = None
    PHZ: Optional[float] = None
    YJZ: Optional[float] = None
    YXP: Optional[float] = None
    XJK: Optional[float] = None
    SRXYLZL: Optional[float] = None
    GE: Optional[float] = None
    ZG: Optional[float] = None
    ZS: Optional[float] = None
    QIAN: Optional[float] = None
    GE_CHROME: Optional[float] = None


class AnalysisResultResponse(BaseModel):
    ID: int
    RWID: int
    DKID: int
    RZ: Optional[float] = None
    PHZ: Optional[float] = None
    YJZ: Optional[float] = None
    YXP: Optional[float] = None
    XJK: Optional[float] = None
    SRXYLZL: Optional[float] = None
    GE: Optional[float] = None
    ZG: Optional[float] = None
    ZS: Optional[float] = None
    QIAN: Optional[float] = None
    GE_CHROME: Optional[float] = None
    SFSC: int = 0

    class Config:
        from_attributes = True
