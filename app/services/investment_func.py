from datetime import datetime
from typing import Optional, Type, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import app.services.validators as vld
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject, Donation, InvestmentBaseModel, User
from app.schemas.charity_project import CharityProjectDB, CharityProjectUpdate


class InvestmentHandler:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    async def close_entity(obj: InvestmentBaseModel) -> InvestmentBaseModel:
        obj.invested_amount = obj.full_amount
        obj.fully_invested = True
        obj.close_date = datetime.now()
        return obj

    async def distribute(
            self,
            recipient: InvestmentBaseModel,
            source: InvestmentBaseModel
    ) -> tuple[InvestmentBaseModel, InvestmentBaseModel]:
        rem_recipient = recipient.full_amount - recipient.invested_amount
        rem_source = source.full_amount - source.invested_amount

        if rem_recipient > rem_source:
            recipient.invested_amount += rem_source
            source = await self.close_entity(source)
        elif rem_recipient == rem_source:
            recipient = await self.close_entity(recipient)
            source = await self.close_entity(source)
        else:
            source.invested_amount += rem_recipient
            recipient = await self.close_entity(recipient)

        return recipient, source

    async def perform_investment(
            self,
            obj_in: InvestmentBaseModel,
            model_db: Type[Union[Donation, CharityProject]]
    ) -> InvestmentBaseModel:
        result = await self.session.execute(
            select(model_db).where(
                model_db.fully_invested == False  # noqa: E712
            ).order_by(model_db.create_date)
        )
        sources = result.scalars().all()

        for source in sources:
            obj_in, source = await self.distribute(obj_in, source)
            self.session.add(obj_in)
            self.session.add(source)

        await self.session.commit()
        await self.session.refresh(obj_in)
        return obj_in


class InvestmentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.handler = InvestmentHandler(session)

    async def create_object(
            self,
            obj_in,
            model,
            user: Optional[User] = None,
            need_for_commit: bool = True
    ) -> InvestmentBaseModel:
        obj_data = obj_in.dict()

        if 'name' in obj_data:
            await vld.check_charity_project_name_duplicate(
                obj_data['name'], self.session
            )

        if user is not None:
            obj_data['user_id'] = user.id

        db_obj = model(**obj_data)

        if not need_for_commit and model is CharityProject:
            db_obj.invested_amount = 0
            db_obj.fully_invested = False

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)

        model_in = Donation if model is CharityProject else CharityProject
        return await self.handler.perform_investment(db_obj, model_in)

    async def update_charity_project(
            self,
            charity_project: CharityProject,
            obj_in: CharityProjectUpdate
    ) -> CharityProjectDB:
        await vld.check_charity_project_is_open(charity_project)

        if obj_in.full_amount is not None:
            vld.check_new_full_amount(
                charity_project.invested_amount,
                obj_in.full_amount
            )

        if obj_in.name:
            await vld.check_charity_project_name_duplicate(
                obj_in.name, self.session
            )

        if (obj_in.full_amount is not None and
                obj_in.full_amount == charity_project.invested_amount):
            charity_project.fully_invested = True
            charity_project.close_date = datetime.now()

        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(charity_project, field, value)

        return await charity_project_crud.update(charity_project, self.session)
