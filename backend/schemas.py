from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


# --- Notices ---
class NoticeBase(BaseModel):
    title: str
    content: str
    is_pinned: int = 0


class NoticeCreate(NoticeBase):
    pass


class NoticeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_pinned: Optional[int] = None


class NoticeOut(NoticeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class NoticeListOut(BaseModel):
    items: List[NoticeOut]
    total: int
    page: int
    limit: int


# --- News ---
class NewsBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None


class NewsCreate(NewsBase):
    pass


class NewsUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None


class NewsOut(NewsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# --- Gallery ---
class GalleryBase(BaseModel):
    title: str
    image_url: str
    category: str = "all"


class GalleryOut(GalleryBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
