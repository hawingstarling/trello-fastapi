from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic import EmailStr
from app.schemas.responses.organization import OrganizationResponse

from app.schemas.model import CustomModel

class OrganizationLimitBase(CustomModel):
  count: int = 0

class OrganizationSubscriptionBase(CustomModel):
  stripe_customer_id: Optional[str] = None
  stripe_subscription_id: Optional[str] = None
  stripe_price_id: Optional[str] = None
  stripe_current_period_end: Optional[datetime] = None

class OrganizationMembershipBase(CustomModel):
  is_admin: bool = False

class OrganizationMembershipCreate(OrganizationMembershipBase):
  organization_id: UUID
  user_id: UUID

class OrganizationBase(CustomModel):
  name: str

class OrganizationCreate(OrganizationBase):
  pass

class OrganizationUpdate(CustomModel):
  name: Optional[str] = None

class InviteMemberRequest(CustomModel):
  email: EmailStr

class RemoveMemberRequest(CustomModel):
  user_id: UUID

class UpdateRoleRequest(CustomModel):
  user_id: UUID
  role: str

class TransferOwnershipRequest(CustomModel):
  new_owner_id: UUID

class PaginatedOrganizationResponse(CustomModel):
  items: List[OrganizationResponse]
  total: int
  page: int
  page_size: int
  pages: int