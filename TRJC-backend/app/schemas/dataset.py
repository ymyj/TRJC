from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class FarmlandDatasetBase(BaseModel):
    RWID: int
    DKID: int
    RWMC: Optional[str] = None
    TBH: Optional[str] = None
    JD: Optional[float] = None
    WD: Optional[float] = None
    CYRQ: Optional[date] = None
    DXBW: Optional[str] = None
    YXTCHD: Optional[float] = None
    GCZD: Optional[str] = None
    RZ: Optional[float] = None
    ZDGX: Optional[str] = None
    SWDYX: Optional[str] = None
    NTLW: Optional[str] = None
    ZAYS: Optional[str] = None
    GGNL: Optional[str] = None
    PSNL: Optional[str] = None
    PHZ: Optional[float] = None
    YJZ: Optional[float] = None
    YXL: Optional[float] = None
    SXJ: Optional[float] = None
    SRXYLZL: Optional[float] = None
    DLMC: Optional[str] = None
    JQCD: Optional[str] = None
    BZ: Optional[str] = None
    GD: Optional[float] = None
    ZG: Optional[float] = None
    ZS: Optional[float] = None
    Q: Optional[float] = None
    G: Optional[float] = None
    GDZLDJ: Optional[float] = None
    ZLFJ: Optional[str] = None


class FarmlandDatasetCreate(FarmlandDatasetBase):
    pass


class FarmlandDatasetUpdate(BaseModel):
    RWMC: Optional[str] = None
    TBH: Optional[str] = None
    JD: Optional[float] = None
    WD: Optional[float] = None
    CYRQ: Optional[date] = None
    DXBW: Optional[str] = None
    YXTCHD: Optional[float] = None
    GCZD: Optional[str] = None
    RZ: Optional[float] = None
    ZDGX: Optional[str] = None
    SWDYX: Optional[str] = None
    NTLW: Optional[str] = None
    ZAYS: Optional[str] = None
    GGNL: Optional[str] = None
    PSNL: Optional[str] = None
    PHZ: Optional[float] = None
    YJZ: Optional[float] = None
    YXL: Optional[float] = None
    SXJ: Optional[float] = None
    SRXYLZL: Optional[float] = None
    DLMC: Optional[str] = None
    JQCD: Optional[str] = None
    BZ: Optional[str] = None
    GD: Optional[float] = None
    ZG: Optional[float] = None
    ZS: Optional[float] = None
    Q: Optional[float] = None
    G: Optional[float] = None
    GDZLDJ: Optional[float] = None
    ZLFJ: Optional[str] = None


class FarmlandDatasetResponse(BaseModel):
    ID: int
    RWID: int
    DKID: int
    RWMC: Optional[str] = None
    TBH: Optional[str] = None
    JD: Optional[float] = None
    WD: Optional[float] = None
    CYRQ: Optional[date] = None
    DXBW: Optional[str] = None
    YXTCHD: Optional[float] = None
    GCZD: Optional[str] = None
    RZ: Optional[float] = None
    ZDGX: Optional[str] = None
    SWDYX: Optional[str] = None
    NTLW: Optional[str] = None
    ZAYS: Optional[str] = None
    GGNL: Optional[str] = None
    PSNL: Optional[str] = None
    PHZ: Optional[float] = None
    YJZ: Optional[float] = None
    YXL: Optional[float] = None
    SXJ: Optional[float] = None
    SRXYLZL: Optional[float] = None
    DLMC: Optional[str] = None
    JQCD: Optional[str] = None
    BZ: Optional[str] = None
    GD: Optional[float] = None
    ZG: Optional[float] = None
    ZS: Optional[float] = None
    Q: Optional[float] = None
    G: Optional[float] = None
    GDZLDJ: Optional[float] = None
    ZLFJ: Optional[str] = None
    SFSC: int = 0

    class Config:
        from_attributes = True
