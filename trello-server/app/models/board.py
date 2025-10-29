import uuid
from datetime import datetime, timedelta

from sqlalchemy import (
  Text, 
  Index,
  String, 
  Column, 
  Integer, 
  DateTime,
  ForeignKey, 
  UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base

class Board(Base):
  __tablename__ = "board"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
  organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=False)
  title = Column(String(255), nullable=False)
  image_id = Column(String(255))
  image_thumb_url = Column(Text)
  image_full_url = Column(Text)
  image_username = Column(Text)
  image_link_html = Column(Text)

  organization = relationship("Organization", back_populates="boards")
  lists = relationship("List", back_populates="board", cascade="all, delete-orphan")

class List(Base):
  __tablename__ = "list"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
  board_id = Column(UUID(as_uuid=True), ForeignKey("board.id"), nullable=False)
  title = Column(String(255), nullable=False)
  order = Column(Integer, nullable=False)

  board = relationship("Board", back_populates="lists")
  cards = relationship("Card", back_populates="list", cascade="all, delete-orphan")

  __table_args__ = (
    UniqueConstraint("board_id", "order", name="unique_list_order_in_board")
  )

class Card(Base):
  __tablename__ = "card"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
  list_id = Column(UUID(as_uuid=True), ForeignKey("list.id"), nullable=False)
  title = Column(String(255), nullable=False)
  order = Column(Integer, nullable=False)
  description = Column(Text, nullable=True)

  list = relationship("List", back_populates="cards")
  edit_lock = relationship("CardEditLock", back_populates="card", uselist=False)

  __table_args__ = (
    UniqueConstraint("list_id", "order", name="unique_card_order_in_list")
  )

class CardEditLock(Base):
  __tablename__ = "card_edit_lock"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
  card_id = Column(UUID(as_uuid=True), ForeignKey("card.id"), nullable=False, unique=True)
  locked_by_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
  locked_at = Column(DateTime(timezone=True), server_default=func.now())
  last_activity = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  card = relationship("Card", back_populates="edit_lock")
  locked_by = relationship("User", back_populates="card_locks")

  __table_args__ = (
    Index('ix_card_edit_lock_card_locked_by', 'card_id', 'locked_by_id'),
    Index('ix_card_edit_lock_last_activity', 'last_activity'),
  )

  @property
  def is_expired(self) -> bool:
    """
    Check if lock has expired (5 minutes timeout)
    """
    return datetime.now() > self.last_activity + timedelta(minutes=5)