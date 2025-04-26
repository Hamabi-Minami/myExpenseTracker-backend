from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean

from app.database.base import Base


class BaseModel(Base):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = Column(Boolean, default=False)
