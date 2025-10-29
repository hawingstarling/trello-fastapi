from pydantic import BaseModel, ConfigDict

class CustomModel(BaseModel):
  """Custom base model with common configuration"""
  model_config = ConfigDict(
    from_attributes=True,
    populate_by_name=True,
  )