from uuid import UUID

from app.models.audit_logs import AuditLog
from app.repositories import AuditLogRepository

from core.controller import BaseController

class AuditLogController(BaseController[AuditLog]):
  def __init__(self, audit_log_repository: AuditLogRepository):
      super().__init__(model=AuditLog, repository=audit_log_repository)
      self.audit_log_repository = audit_log_repository

  async def get_by_organization(
      self, org_id: UUID, skip: int = 0, limit: int = 100
  ) -> list[AuditLog]:
      return await self.audit_log_repository.get_by_organization(
          org_id, skip, limit
      )
