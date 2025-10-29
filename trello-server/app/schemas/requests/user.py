from uuid import UUID
from typing import Optional
from pydantic import EmailStr

from app.schemas.model import CustomModel

class UserPublicData(CustomModel):
  id: UUID
  first_name = Optional[str] = None
  last_name = Optional[str] = None
  email = EmailStr
  identifier: str
  