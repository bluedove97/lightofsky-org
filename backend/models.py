from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, func
from sqlalchemy.dialects.mysql import TINYINT
from database import Base


class Notice(Base):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    is_pinned = Column(TINYINT(1), default=0)
    created_at = Column(DateTime, default=datetime.now, server_default=func.now())
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now,
                        server_default=func.now())


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.now, server_default=func.now())
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now,
                        server_default=func.now())


class Gallery(Base):
    __tablename__ = "gallery"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    image_url = Column(String(500), nullable=False)
    category = Column(
        Enum("all", "worship", "events", "retreats", "service"), default="all"
    )
    created_at = Column(DateTime, default=datetime.now, server_default=func.now())
