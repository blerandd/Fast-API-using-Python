from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from .db import Base


class TodoModel(Base):
    __tablename__ = "todos"

    todo_id = Column(Integer, primary_key=True, index=True)
    todo_name = Column(String(512), nullable=False)
    todo_description = Column(String(2000), nullable=False)
    priority = Column(Integer, nullable=False, default=3)

    status = Column(String(32), nullable=False, default="NEW")
    due_date = Column(DateTime(timezone=True), nullable=True)

    is_deleted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
