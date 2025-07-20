from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, UTC

from .database import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    role = Column(String,nullable=False, default="user")
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
