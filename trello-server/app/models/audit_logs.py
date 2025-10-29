import uuid

from enum import Enum

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from core.database import Base

class Action(str, Enum):
  CREATE = "CREATE"
  UPDATE = "UPDATE" 
  DELETE = "DELETE"

class EntityType(str, Enum):
  BOARD = "BOARD"
  LIST = "LIST"
  CARD = "CARD"
  USER = "USER"
  ORGANIZATION = "ORGANIZATION"

class AuditLog(Base):
  __tablename__ = "audit_logs"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
  organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=False)

  action = Column(String(10), nullable=False) 
  entity_id = Column(String(255), nullable=False)
  entity_type = Column(String(10), nullable=False) 
  entity_title = Column(String(255), nullable=False)
  user_id = Column(String(255), nullable=False)
  user_image = Column(Text)
  user_name = Column(Text, nullable=False)

  organization = relationship("Organization", back_populates="audit_logs")




