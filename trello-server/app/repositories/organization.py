from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from app.models.organization import Organization, OrganizationUser, OrganizationOwner, OrganizationLimit

from core.repository import BaseRepository

class OrganizationRepository(BaseRepository[Organization]):
  """
  Organization repository provides all database operations for Organization model.
  """
  async def get_by_slug(self, slug: str, join_: set[str] | None = None) -> Organization | None:
    query = await self._query(join_)
    query = query.filter(Organization.slug == slug)

    if join_ is not None:
      return await self._all_unique(query)
    return await self._one_or_none(query)
  
  def _join_users(self, query: Select) -> Select:
        return query.options(joinedload(Organization.users))

  def _join_limit(self, query: Select) -> Select:
      return query.options(joinedload(Organization.limit))

  def _join_subscription(self, query: Select) -> Select:
      return query.options(joinedload(Organization.subscription))
  
class OrganizationUserRepository(BaseRepository[OrganizationUser]):
  """OrganizationUser repository."""

  async def get_by_org_and_user(
      self, org_id, user_id, join_: set[str] | None = None
  ) -> OrganizationUser | None:
      query = await self._query(join_)
      query = query.filter(
          OrganizationUser.organization_id == org_id,
          OrganizationUser.user_id == user_id
      )
      
      if join_ is not None:
          return await self._all_unique(query)
      return await self._one_or_none(query)

  def _join_organization(self, query: Select) -> Select:
      return query.options(joinedload(OrganizationUser.organization))

  def _join_user(self, query: Select) -> Select:
      return query.options(joinedload(OrganizationUser.user))