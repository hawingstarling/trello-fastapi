from uuid import UUID

from app.models.organization import Organization, OrganizationUser
from app.repositories import OrganizationRepository, OrganizationUserRepository

from core.controller import BaseController
from core.database import Propagation, Transactional
from core.exceptions import BadRequestException, NotFoundException

class OrganizationController(BaseController[Organization]):
  def __init__(
    self, 
    organization_repository : OrganizationRepository, 
    organization_user_repository: OrganizationUserRepository,
  ):
    super().__init__(model=Organization, repository=organization_repository)
    self.organization_repository = organization_repository
    self.organization_user_repository = organization_user_repository

  async def get_by_slug(self, slug: str) -> Organization:
    org = await self.organization_repository.get_by_slug(slug)
    if not org:
      raise NotFoundException(
        f"Organization with slug {slug} not found"
      )
    return org
  
  async def get_user_organizations(self, user_id: UUID) -> list[Organization]:
    """Get all organizations that user is member of"""
    # This would need a custom query in repository
    pass

  @Transactional(propagation=Propagation.REQUIRED)
  async def add_member(
    self, org_id: UUID, user_id: UUID, is_admin: bool = False
  ) -> OrganizationUser:
    # Check if already member
    existing = await self.organization_user_repository.get_by_org_and_user(
      org_id, user_id
    )
    if existing:
      raise BadRequestException("User is already a member")
    
    return await self.organization_user_repository.create({
      "organization_id": org_id,
      "user_id": user_id,
      "is_admin": is_admin
    })
  
  @Transactional(propagation=Propagation.REQUIRED)
  async def remove_member(self, org_id: UUID, user_id: UUID) -> bool:
      member = await self.organization_user_repository.get_by_org_and_user(
          org_id, user_id
      )
      if not member:
          raise NotFoundException("Member not found")
      
      await self.organization_user_repository.delete(member)
      return True