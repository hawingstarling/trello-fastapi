from typing import Optional, List
from uuid import UUID
from pydantic import field_validator

from core.schemas import CustomModel

class CardBase(CustomModel):
  title: str
  order: int
  description: Optional[str] = None

class CardCreate(CardBase):
  list_id: UUID

class CardUpdate(CustomModel):
  title: Optional[str] = None
  order: Optional[int] = None
  description: Optional[str] = None

class ListBase(CustomModel):
  title: str
  order: int


class ListCreate(ListBase):
  board_id: UUID


class ListUpdate(CustomModel):
  title: Optional[str] = None
  order: Optional[int] = None

class BoardBase(CustomModel):
  title: str
  image_id: Optional[str] = None
  image_thumb_url: Optional[str] = None
  image_full_url: Optional[str] = None
  image_username: Optional[str] = None
  image_link_html: Optional[str] = None

class BoardCreate(BoardBase):
  organization_id: UUID


class BoardUpdate(CustomModel):
  title: Optional[str] = None
  image_id: Optional[str] = None
  image_thumb_url: Optional[str] = None
  image_full_url: Optional[str] = None
  image_username: Optional[str] = None
  image_link_html: Optional[str] = None

class UpdateOrderItem(CustomModel):
  id: UUID
  order: int

  @field_validator('order')
  @classmethod
  def validate_order(cls, v):
    if v < 0:
        raise ValueError('Order must be >= 0')
    return v


class UpdateOrderRequest(CustomModel):
  items: List[UpdateOrderItem]


class MoveCardRequest(CustomModel):
  destination_list_id: UUID
  order: int

  @field_validator('order')
  @classmethod
  def validate_order(cls, v):
    if v < 0:
        raise ValueError('Order must be >= 0')
    return v
  

