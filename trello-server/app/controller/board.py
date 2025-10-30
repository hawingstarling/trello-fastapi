from uuid import UUID

from sqlalchemy import func

from app.models.board import Board, List, Card, CardEditLock
from app.repositories import (
    BoardRepository, 
    ListRepository, 
    CardRepository,
    CardEditLockRepository
)

from core.controller import BaseController
from core.database import Propagation, Transactional
from core.exceptions import BadRequestException, NotFoundException

class BoardController(BaseController[Board]):
  def __init__(self, board_repository: BoardRepository):
    super().__init__(model=Board, repository=board_repository)
    self.board_repository = board_repository

  async def get_by_organization(
    self, org_id: UUID, skip: int = 0, limit: int = 100
  ) -> list[Board]:
    return await self.board_repository.get_by_organization(org_id, skip, limit)
  
class ListController(BaseController[List]):
  def __init__(self, list_repository: ListRepository):
    super().__init__(model=List, repository=list_repository)
    self.list_repository = list_repository

  async def get_by_board(self, board_id: UUID) -> list[List]:
    return await self.list_repository.get_by_board(board_id)

  @Transactional(propagation=Propagation.REQUIRED)
  async def reorder(self, items: list[dict]) -> int:
    """Reorder lists"""
    updated_count = 0
    for item in items:
        list_obj = await self.get_by_id(item['id'])
        if list_obj:
            list_obj.order = item['order']
            updated_count += 1
    return updated_count
  
class CardController(BaseController[Card]):
    def __init__(self, card_repository: CardRepository):
        super().__init__(model=Card, repository=card_repository)
        self.card_repository = card_repository

    async def get_by_list(self, list_id: UUID) -> list[Card]:
        return await self.card_repository.get_by_list(list_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def move_to_list(
        self, card_id: UUID, destination_list_id: UUID, order: int
    ) -> Card:
        """Move card to another list"""
        card = await self.get_by_id(card_id)
        card.list_id = destination_list_id
        card.order = order
        return card


class CardEditLockController(BaseController[CardEditLock]):
    def __init__(self, lock_repository: CardEditLockRepository):
        super().__init__(model=CardEditLock, repository=lock_repository)
        self.lock_repository = lock_repository

    async def get_by_card(self, card_id: UUID) -> CardEditLock | None:
        return await self.lock_repository.get_by_card(card_id)

    async def get_by_card_and_user(
        self, card_id: UUID, user_id: UUID
    ) -> CardEditLock | None:
        return await self.lock_repository.get_by_card_and_user(card_id, user_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def acquire_lock(self, card_id: UUID, user_id: UUID) -> CardEditLock:
        """Acquire edit lock for card"""
        # Check if already locked
        existing_lock = await self.get_by_card(card_id)
        
        if existing_lock:
            if existing_lock.locked_by_id == user_id:
                # Refresh activity
                existing_lock.last_activity = func.now()
                return existing_lock
            elif not existing_lock.is_expired:
                raise BadRequestException(
                    f"Card is locked by another user"
                )
            else:
                # Lock expired, delete it
                await self.lock_repository.delete(existing_lock)
        
        # Create new lock
        return await self.lock_repository.create({
            "card_id": card_id,
            "locked_by_id": user_id
        })

    @Transactional(propagation=Propagation.REQUIRED)
    async def release_lock(self, card_id: UUID, user_id: UUID) -> bool:
        """Release edit lock"""
        lock = await self.get_by_card_and_user(card_id, user_id)
        if lock:
            await self.lock_repository.delete(lock)
            return True
        return False

    @Transactional(propagation=Propagation.REQUIRED)
    async def maintain_lock(self, card_id: UUID, user_id: UUID) -> CardEditLock:
        """Maintain/refresh edit lock"""
        lock = await self.get_by_card_and_user(card_id, user_id)
        if not lock:
            raise NotFoundException("No active lock found")
        
        if lock.is_expired:
            await self.lock_repository.delete(lock)
            raise BadRequestException("Lock has expired")
        
        # Refresh activity
        lock.last_activity = func.now()
        return lock
  
