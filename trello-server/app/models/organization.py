import uuid

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin

class Organization(Base, TimestampMixin):
  __tablename__ = "organization"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
  name = Column(String(200), nullable=False)
  slug = Column(String(200), nullable=False, unique=True)

  users = relationship("OrganizationUser", back_populates="organizations")
  organization_owners = relationship("OrganizationOwner", back_populates="organization")
  limit = relationship("OrganizationLimit", back_populates="organization", uselist=False)
  subscription = relationship("OrganizationSubscription", back_populates="organization", uselist=False)

class OrganizationUser(Base, TimestampMixin):
  __tablename__ = "organization_user"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
  organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=False)
  user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
  is_admin = Column(Boolean, default=False)

  organization = relationship("Organization", back_populates="organization_users")
  user = relationship("User", back_populates="organization_users")
  organization_owners = relationship("OrganizationOwner", back_populates="organization_user")

class OrganizationOwner(Base):
  __tablename__ = "organization_owner"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
  organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=False)
  organization_user_id = Column(UUID(as_uuid=True), ForeignKey("organization_user.id"), nullable=False)

  organization = relationship("Organization", back_populates="organization_owners")
  organization_user = relationship("OrganizationUser", back_populates="organization_owners")

class OrganizationLimit(Base):
  __tablename__ = "organization_limit"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
  organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=False, unique=True)
  count = Column(Integer, default=0)

  organization = relationship("Organization", back_populates="limit")

