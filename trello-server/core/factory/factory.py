from functools import partial
from fastapi import Depends

from app.controller import (
    OrganizationController,
    BoardController,
    ListController,
    CardController,
    CardEditLockController,
    AuditLogController,
)
from app.models.organization import Organization, OrganizationUser
from app.models.board import Board, List, Card, CardEditLock
from app.models.audit_logs import AuditLog
from app.repositories import (
    OrganizationRepository,
    OrganizationUserRepository,
    BoardRepository,
    ListRepository,
    CardRepository,
    CardEditLockRepository,
    AuditLogRepository,
)
from core.database import get_session

class Factory:
  """
  Factory container that instantiates all controllers and repositories
  """

  # Repositories
  organization_repository = partial(OrganizationRepository, Organization)
  organization_user_repository = partial(OrganizationUserRepository, OrganizationUser)
  board_repository = partial(BoardRepository, Board)
  list_repository = partial(ListRepository, List)
  card_repository = partial(CardRepository, Card)
  card_edit_lock_repository = partial(CardEditLockRepository, CardEditLock)
  audit_log_repository = partial(AuditLogRepository, AuditLog)

  # Organization Controllers
  def get_organization_controller(self, db_session=Depends(get_session)):
      return OrganizationController(
          organization_repository=self.organization_repository(db_session=db_session),
          organization_user_repository=self.organization_user_repository(db_session=db_session)
      )

  # Board Controllers
  def get_board_controller(self, db_session=Depends(get_session)):
      return BoardController(
          board_repository=self.board_repository(db_session=db_session)
      )

  def get_list_controller(self, db_session=Depends(get_session)):
      return ListController(
          list_repository=self.list_repository(db_session=db_session)
      )

  def get_card_controller(self, db_session=Depends(get_session)):
      return CardController(
          card_repository=self.card_repository(db_session=db_session)
      )

  def get_card_edit_lock_controller(self, db_session=Depends(get_session)):
      return CardEditLockController(
          lock_repository=self.card_edit_lock_repository(db_session=db_session)
      )

  # Audit Log Controller
  def get_audit_log_controller(self, db_session=Depends(get_session)):
      return AuditLogController(
          audit_log_repository=self.audit_log_repository(db_session=db_session)
      )