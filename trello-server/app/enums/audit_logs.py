from enum import Enum


class Action(str, Enum):
  CREATE = "CREATE"
  UPDATE = "UPDATE" 
  DELETE = "DELETE"


class EntityType(str, Enum):
  BOARD = "BOARD"
  LIST = "LIST"
  CARD = "CARD"
  USER = "USER"
  ORGANIZATION = "ORGANIZATION"