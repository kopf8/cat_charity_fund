from sqlalchemy import Column, String, Text

from app.models.base import InvestmentBaseModel


class CharityProject(InvestmentBaseModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'Project name: {self.name}, '
            f'Project description: {self.description}, '
            f'{super().__repr__()}'
        )
