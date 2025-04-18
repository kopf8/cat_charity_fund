from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import app.services.validators as vld
from app.models import CharityProject


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    @staticmethod
    async def update(
            charity_project: CharityProject,
            session: AsyncSession,
    ):
        session.add(charity_project)
        await session.commit()
        await session.refresh(charity_project)
        return charity_project

    @staticmethod
    async def remove(
            charity_project: CharityProject,
            session: AsyncSession
    ):
        await vld.check_charity_project_is_open(charity_project)
        await vld.check_charity_project_invested(charity_project)
        await session.delete(charity_project)
        await session.commit()
        return charity_project

    async def get_all_open(
            self,
            session: AsyncSession
    ):
        open_projects = await session.execute(
            select(self.model).where(self.model.fully_invested == 0).order_by(
                self.model.create_date)
        )
        return open_projects.scalars().all()
