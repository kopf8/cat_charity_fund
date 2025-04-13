from sqlalchemy import Column, String, Text

from app.core.config import Constants
from app.models.base import InvestmentBaseModel


class CharityProject(InvestmentBaseModel):
    name = Column(String(Constants.NAME_MAX_LEN), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'Project name: {self.name}, '
            f'Project description: {self.description}, '
            f'{super().__repr__()}'
        )
