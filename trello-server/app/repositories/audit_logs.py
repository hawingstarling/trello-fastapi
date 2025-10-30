from sqlalchemy import Select
from sqlalchemy.orm import joinedload
from app.models.audit_logs import AuditLog
from core.repository import BaseRepository


class AuditLogRepository(BaseRepository[AuditLog]):
  """AuditLog repository."""

  async def get_by_organization(
      self, org_id, skip: int = 0, limit: int = 100, join_: set[str] | None = None
  ) -> list[AuditLog]:
      query = await self._query(join_)
      query = query.filter(AuditLog.organization_id == org_id).order_by(
          AuditLog.created_at.desc()
      ).offset(skip).limit(limit)
      
      if join_ is not None:
          return await self._all_unique(query)
      return await self._all(query)

  def _join_organization(self, query: Select) -> Select:
      return query.options(joinedload(AuditLog.organization))
