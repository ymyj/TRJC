from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TaskInfoBase(BaseModel):
    RWMC: str
    RWLX: str
    SSQH: Optional[str] = None
    FZR: Optional[str] = None
    JHKSSJ: Optional[str] = None
    LXDH: Optional[str] = None
    RWMS: Optional[str] = None
    plot_ids: Optional[List[int]] = None


class TaskInfoCreate(TaskInfoBase):
    pass


class TaskInfoUpdate(BaseModel):
    RWMC: Optional[str] = None
    RWLX: Optional[str] = None
    SSQH: Optional[str] = None
    FZR: Optional[str] = None
    JHKSSJ: Optional[str] = None
    LXDH: Optional[str] = None
    RWMS: Optional[str] = None
    ZT: Optional[str] = None
    plot_ids: Optional[List[int]] = None


class TaskInfoResponse(BaseModel):
    ID: int
    RWBH: str
    RWMC: str
    RWLX: str
    SSQH: Optional[str] = None
    FZR: Optional[str] = None
    JHKSSJ: Optional[str] = None
    LXDH: Optional[str] = None
    RWMS: Optional[str] = None
    ZT: str
    CJSJ: Optional[datetime] = None
    SFSC: int = 0

    class Config:
        from_attributes = True


class TaskStatsResponse(BaseModel):
    total: int = 0
    pending: int = 0
    processing: int = 0
    completed: int = 0


class TaskAttachmentResponse(BaseModel):
    ID: int
    RWID: int
    FILE_NAME: str
    FILE_PATH: str
    FILE_SIZE: Optional[int] = None
    FILE_TYPE: Optional[str] = None
    CJSJ: Optional[datetime] = None

    class Config:
        from_attributes = True
