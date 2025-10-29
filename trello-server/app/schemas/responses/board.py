from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.schemas.requests.board import BoardBase, CardBase, ListBase
from core.schemas import CustomModel

class CardResponse(CardBase):
  id: UUID
  list_id: UUID
  created_at: datetime
  updated_at: datetime

class ListResponse(ListBase):
  id: UUID
  board_id: UUID
  card_count: int
  created_at: datetime
  updated_at: datetime

class ListDetailResponse(ListResponse):
  cards: List[CardResponse] = []

class BoardResponse(BoardBase):
  id: UUID
  organization_id: UUID
  list_count: int
  created_at: datetime
  updated_at: datetime


class BoardDetailResponse(BoardResponse):
  lists: List[ListDetailResponse] = []

class CardEditLockResponse(CustomModel):
  is_editable: bool
  locked_by: Optional[UUID] = None
  locked_by_username: Optional[str] = None
  locked_at: Optional[datetime] = None
  message: str


class CardEditLockMaintainResponse(CardEditLockResponse):
  last_activity: Optional[datetime] = None