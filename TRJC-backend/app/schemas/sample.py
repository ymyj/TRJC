from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class SampleRecordBase(BaseModel):
    RWID: int
    DKID: int
    TRHHYPBH: Optional[str] = None
    DLWZ: Optional[str] = None
    DLZB_D1BH: Optional[str] = None
    DLZB_D1JD: Optional[str] = None
    DLZB_D1WD: Optional[str] = None
    DLZB_D2BH: Optional[str] = None
    DLZB_D2JD: Optional[str] = None
    DLZB_D2WD: Optional[str] = None
    DLZB_D3BH: Optional[str] = None
    DLZB_D3JD: Optional[str] = None
    DLZB_D3WD: Optional[str] = None
    CYSD_D1: Optional[str] = None
    CYSD_D2: Optional[str] = None
    CYSD_D3: Optional[str] = None
    CYDWSL: Optional[str] = None
    HHYPSL: Optional[str] = None
    CYRQ: Optional[str] = None
    CYRY: Optional[str] = None
    XMDWDB: Optional[str] = None
    TKZJ: Optional[str] = None


class SampleRecordCreate(SampleRecordBase):
    pass


class SampleRecordUpdate(BaseModel):
    TRHHYPBH: Optional[str] = None
    DLWZ: Optional[str] = None
    DLZB_D1BH: Optional[str] = None
    DLZB_D1JD: Optional[str] = None
    DLZB_D1WD: Optional[str] = None
    DLZB_D2BH: Optional[str] = None
    DLZB_D2JD: Optional[str] = None
    DLZB_D2WD: Optional[str] = None
    DLZB_D3BH: Optional[str] = None
    DLZB_D3JD: Optional[str] = None
    DLZB_D3WD: Optional[str] = None
    CYSD_D1: Optional[str] = None
    CYSD_D2: Optional[str] = None
    CYSD_D3: Optional[str] = None
    CYDWSL: Optional[int] = None
    HHYPSL: Optional[float] = None
    CYRQ: Optional[date] = None
    CYRY: Optional[str] = None
    XMDWDB: Optional[str] = None
    TKZJ: Optional[str] = None


class SampleRecordResponse(BaseModel):
    ID: int
    RWID: int
    DKID: int
    TRHHYPBH: Optional[str] = None
    DLWZ: Optional[str] = None
    DLZB_D1BH: Optional[str] = None
    DLZB_D1JD: Optional[str] = None
    DLZB_D1WD: Optional[str] = None
    DLZB_D2BH: Optional[str] = None
    DLZB_D2JD: Optional[str] = None
    DLZB_D2WD: Optional[str] = None
    DLZB_D3BH: Optional[str] = None
    DLZB_D3JD: Optional[str] = None
    DLZB_D3WD: Optional[str] = None
    CYSD_D1: Optional[str] = None
    CYSD_D2: Optional[str] = None
    CYSD_D3: Optional[str] = None
    CYDWSL: Optional[int] = None
    HHYPSL: Optional[float] = None
    CYRQ: Optional[date] = None
    CYRY: Optional[str] = None
    XMDWDB: Optional[str] = None
    TKZJ: Optional[str] = None
    SFSC: int = 0

    class Config:
        from_attributes = True
