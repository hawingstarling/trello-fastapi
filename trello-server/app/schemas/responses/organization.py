from uuid import UUID
from datetime import datetime
from typing import Optional, List

from app.schemas.requests.organization import (
  OrganizationBase,
  OrganizationLimitBase,
  OrganizationMembershipBase,
  OrganizationSubscriptionBase,
  
)
from app.schemas.requests.user import UserPublicData

class OrganizationLimitResponse(OrganizationLimitBase):
  id: UUID
  organization_id: UUID
  created_at: datetime
  updated_at: datetime

class OrganizationSubscriptionResponse(OrganizationSubscriptionBase):
  id: UUID
  organization_id: UUID
  created_at: datetime
  updated_at: datetime

class OrganizationMembershipResponse(OrganizationMembershipBase):
  id: UUID
  organization_id: UUID
  user_id: UUID
  public_user_data: UserPublicData
  role: str 
  created_at: datetime
  updated_at: datetime

class OrganizationResponse(OrganizationBase):
  id: UUID
  slug: str
  is_active: bool = True
  created_at: datetime
  updated_at: datetime
  member_count: Optional[int] = None
  limit: Optional[OrganizationLimitResponse] = None
  subscription: Optional[OrganizationSubscriptionResponse] = None

class OrganizationDetailResponse(OrganizationResponse):
  memberships: List[OrganizationMembershipResponse] = []

