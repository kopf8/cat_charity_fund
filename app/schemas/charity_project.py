from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint, Extra, Field, validator

from app.core.config import Constants, Messages


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=Constants.NAME_MAX_LEN)
    description: Optional[str] = Field(None)
    full_amount: Optional[conint(gt=0)]

    class Config:
        min_anystr_length = Constants.NAME_MIN_LEN
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=Constants.NAME_MAX_LEN)
    description: str = Field(...)
    full_amount: conint(gt=0)


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
    invested_amount: conint(ge=0) = Field(default=0)
    fully_invested: bool = Field(default=False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
