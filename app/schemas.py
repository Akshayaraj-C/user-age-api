from datetime import date
from pydantic import BaseModel, Field, computed_field
from app.service import calculate_age

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    dob: date

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserResponse(BaseModel):
    id: int
    name: str
    dob: date

    class Config:
        from_attributes = True

    @computed_field
    @property
    def age(self) -> int:
        return calculate_age(self.dob)
