from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import app.api.utils as u
import app.api.validators as vld
from app.models import CharityProject, Donation, User
from app.services.investment_func import perform_investment


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

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
            need_for_commit: Optional[bool] = True
    ):
        obj_in_data = obj_in.dict()
        if obj_in_data.get('name') is not None:
            await vld.check_charity_project_name_duplicate(
                obj_in_data['name'], session
            )
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        if not need_for_commit and self.model is CharityProject:
            db_obj.invested_amount = 0
            db_obj.fully_invested = False
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        model_in = Donation if self.model is CharityProject else CharityProject
        return await perform_investment(
            obj_in=db_obj,
            model_db=model_in,
            session=session
        )

    @staticmethod
    async def update(
            project_id,
            obj_in,
            session: AsyncSession,
    ):
        charity_project = await u.get_project_or_404(project_id, session)
        await vld.check_charity_project_is_open(project_id, session)
        if obj_in.full_amount:
            vld.check_new_full_amount(
                charity_project.invested_amount,
                obj_in.full_amount
            )
        if obj_in.name:
            await vld.check_charity_project_name_duplicate(
                obj_in.name, session
            )
        if obj_in.full_amount:
            if obj_in.full_amount == charity_project.invested_amount:
                setattr(charity_project, 'fully_invested', True)
                setattr(charity_project, 'close_date', datetime.now())
        obj_data = jsonable_encoder(charity_project)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(charity_project, field, update_data[field])
        session.add(charity_project)
        await session.commit()
        await session.refresh(charity_project)
        return charity_project

    @staticmethod
    async def remove(
            project_id,
            session: AsyncSession
    ):
        charity_project = await u.get_project_or_404(
            project_id, session
        )
        await vld.check_charity_project_is_open(
            charity_project.id, session
        )
        await vld.check_charity_project_invested(
            charity_project.id, session
        )
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
