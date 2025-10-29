from uuid import UUID
from datetime import datetime
from typing import List

from core.schemas import CustomModel
from app.schemas.requests.audit_logs import AuditLogBase

class AuditLogResponse(AuditLogBase):
  id: UUID
  organization_id: UUID
  created_at: datetime
  updated_at: datetime
  action_display: str
  entity_type_display: str


class PaginatedAuditLogResponse(CustomModel):
  items: List[AuditLogResponse]
  total: int
  page: int
  page_size: int
  pages: int