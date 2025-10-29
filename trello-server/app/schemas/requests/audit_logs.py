from typing import Optional
from uuid import UUID

from app.schemas.model import CustomModel
from app.enums.audit_logs import Action, EntityType

class AuditLogBase(CustomModel):
  action: Action
  entity_id: str
  entity_type: EntityType
  entity_title: str
  user_id: str
  user_image: Optional[str] = None
  user_name: str

class AuditLogCreate(AuditLogBase):
  organization_id: UUID
