from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.core.config import Constants, Messages


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=Constants.NAME_MAX_LEN)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt]

    class Config:
        min_anystr_length = Constants.NAME_MIN_LEN
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=Constants.NAME_MAX_LEN)
    description: str = Field(...)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    @validator('name')
    def name_cant_be_none(cls, value: Optional[str]):
        if value is None:
            raise ValueError(Messages.PROJECT_NAME_NOT_NULL)
        return value

    @validator('description')
    def description_cant_be_none(cls, value: Optional[str]):
        if value is None:
            raise ValueError(Messages.PROJECT_DESCRIPTION_NOT_NULL)
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
