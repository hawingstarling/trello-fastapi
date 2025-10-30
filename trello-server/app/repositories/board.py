
from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from app.models.board import Board, List, Card, CardEditLock

from core.repository import BaseRepository


class BoardRepository(BaseRepository[Board]):
  """
  Board repository for database operations
  Handles all board-related queries with optimizations
  """
  async def get_by_organization(
    self, org_id, skip: int = 0, limit: int = 100, join_: set[str] | None = None
  ) -> list[Board]:
    query = await self._query(join_)
    query = query.filter(Board.organization_id == org_id).offset(skip).limit(limit)

    if join_ is not None:
      return await self._all_unique(query)
    return await self._all(query)
  
  def _join_organization(self, query: Select) -> Select:
    return query.options(joinedload(Board.organization))
  
  def _join_lists(self, query: Select) -> Select:
    return query.options(joinedload(Board.lists))
  
class ListRepository(BaseRepository[List]):
  """List repository."""

  async def get_by_board(
      self, board_id, join_: set[str] | None = None
  ) -> list[List]:
      query = await self._query(join_)
      query = query.filter(List.board_id == board_id).order_by(List.order)
      
      if join_ is not None:
          return await self._all_unique(query)
      return await self._all(query)

  def _join_board(self, query: Select) -> Select:
      return query.options(joinedload(List.board))

  def _join_cards(self, query: Select) -> Select:
      return query.options(joinedload(List.cards))


class CardRepository(BaseRepository[Card]):
  """Card repository."""

  async def get_by_list(
      self, list_id, join_: set[str] | None = None
  ) -> list[Card]:
      query = await self._query(join_)
      query = query.filter(Card.list_id == list_id).order_by(Card.order)
      
      if join_ is not None:
          return await self._all_unique(query)
      return await self._all(query)

  def _join_list(self, query: Select) -> Select:
      return query.options(joinedload(Card.list))

  def _join_edit_lock(self, query: Select) -> Select:
      return query.options(joinedload(Card.edit_lock))


class CardEditLockRepository(BaseRepository[CardEditLock]):
  """CardEditLock repository."""

  async def get_by_card(
      self, card_id, join_: set[str] | None = None
  ) -> CardEditLock | None:
      query = await self._query(join_)
      query = query.filter(CardEditLock.card_id == card_id)
      
      if join_ is not None:
          return await self._all_unique(query)
      return await self._one_or_none(query)

  async def get_by_card_and_user(
      self, card_id, user_id, join_: set[str] | None = None
  ) -> CardEditLock | None:
      query = await self._query(join_)
      query = query.filter(
          CardEditLock.card_id == card_id,
          CardEditLock.locked_by_id == user_id
      )
      
      if join_ is not None:
          return await self._all_unique(query)
      return await self._one_or_none(query)

  def _join_card(self, query: Select) -> Select:
      return query.options(joinedload(CardEditLock.card))

  def _join_locked_by(self, query: Select) -> Select:
      return query.options(joinedload(CardEditLock.locked_by))

  

  
