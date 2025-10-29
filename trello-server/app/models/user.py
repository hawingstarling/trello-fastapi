import uuid

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base

class User(Base):
  __tablename__ = "user"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
  email = Column(String(255), unique=True, nullable=False, index=True)
  username = Column(String(150), unique=True, nullable=False)
  first_name = Column(String(150))
  last_name = Column(String(150))
  avatar = Column(Text, nullable=True)
  is_active = Column(Boolean, default=True)
  is_staff = Column(Boolean, default=False)
  is_superuser = Column(Boolean, default=False)
  last_login = Column(DateTime(timezone=True), nullable=True)
  date_joined = Column(DateTime(timezone=True), server_default=func.now())
  organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=True)

  organization = relationship("Organization", back_populates="users")
  card_locks = relationship("CardEditLock", back_populates="locked_by")
  organization_users = relationship("OrganizationUser", back_populates="user")
