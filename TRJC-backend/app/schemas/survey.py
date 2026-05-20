from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class SurveyRecordBase(BaseModel):
    RWID: int
    DKID: int
    XMMC: Optional[str] = None
    TBH: Optional[str] = None
    MJ: Optional[float] = None
    DLWZ: Optional[str] = None
    DLZB_JD: Optional[str] = None
    DLZB_WD: Optional[str] = None
    BGQ: Optional[str] = None
    BGSJ: Optional[str] = None
    LYLX: Optional[str] = None
    YXTCHD: Optional[float] = None
    QRLXJHL: Optional[str] = None
    LSHL: Optional[float] = None
    DXPD: Optional[float] = None
    TMPZCD: Optional[str] = None
    SZBZTJ: Optional[str] = None
    DLTXTJ: Optional[str] = None
    DXBW: Optional[str] = None
    ZDGX: Optional[str] = None
    PSNL: Optional[str] = None
    HBGD: Optional[float] = None
    NTFH: Optional[str] = None
    GCHD: Optional[float] = None
    KCRQ: Optional[date] = None
    DCRY: Optional[str] = None
    XMDWDB: Optional[str] = None
    TKZJ: Optional[str] = None


class SurveyRecordCreate(SurveyRecordBase):
    pass


class SurveyRecordUpdate(BaseModel):
    XMMC: Optional[str] = None
    TBH: Optional[str] = None
    MJ: Optional[float] = None
    DLWZ: Optional[str] = None
    DLZB_JD: Optional[str] = None
    DLZB_WD: Optional[str] = None
    BGQ: Optional[str] = None
    BGSJ: Optional[str] = None
    LYLX: Optional[str] = None
    YXTCHD: Optional[float] = None
    QRLXJHL: Optional[str] = None
    LSHL: Optional[float] = None
    DXPD: Optional[float] = None
    TMPZCD: Optional[str] = None
    SZBZTJ: Optional[str] = None
    DLTXTJ: Optional[str] = None
    DXBW: Optional[str] = None
    ZDGX: Optional[str] = None
    PSNL: Optional[str] = None
    HBGD: Optional[float] = None
    NTFH: Optional[str] = None
    GCHD: Optional[float] = None
    KCRQ: Optional[date] = None
    DCRY: Optional[str] = None
    XMDWDB: Optional[str] = None
    TKZJ: Optional[str] = None


class SurveyRecordResponse(BaseModel):
    ID: int
    RWID: int
    DKID: int
    XMMC: Optional[str] = None
    TBH: Optional[str] = None
    MJ: Optional[float] = None
    DLWZ: Optional[str] = None
    DLZB_JD: Optional[str] = None
    DLZB_WD: Optional[str] = None
    BGQ: Optional[str] = None
    BGSJ: Optional[str] = None
    LYLX: Optional[str] = None
    YXTCHD: Optional[float] = None
    QRLXJHL: Optional[str] = None
    LSHL: Optional[float] = None
    DXPD: Optional[float] = None
    TMPZCD: Optional[str] = None
    SZBZTJ: Optional[str] = None
    DLTXTJ: Optional[str] = None
    DXBW: Optional[str] = None
    ZDGX: Optional[str] = None
    PSNL: Optional[str] = None
    HBGD: Optional[float] = None
    NTFH: Optional[str] = None
    GCHD: Optional[float] = None
    KCRQ: Optional[date] = None
    DCRY: Optional[str] = None
    XMDWDB: Optional[str] = None
    TKZJ: Optional[str] = None
    SFSC: int = 0

    class Config:
        from_attributes = True
