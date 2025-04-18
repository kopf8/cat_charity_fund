from datetime import datetime
from typing import Optional, Type, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import app.services.validators as vld
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject, Donation, InvestmentBaseModel, User
from app.schemas.charity_project import CharityProjectDB, CharityProjectUpdate


async def close_entity(
    obj_db: InvestmentBaseModel
) -> InvestmentBaseModel:
    obj_db.invested_amount = obj_db.full_amount
    obj_db.fully_invested = True
    obj_db.close_date = datetime.now()
    return obj_db


async def distribution(
    obj_in: InvestmentBaseModel,
    obj_db: InvestmentBaseModel
) -> tuple[InvestmentBaseModel, InvestmentBaseModel]:
    rem_obj_in = obj_in.full_amount - obj_in.invested_amount
    rem_obj_db = obj_db.full_amount - obj_db.invested_amount
    if rem_obj_in > rem_obj_db:
        obj_in.invested_amount += rem_obj_db
        obj_db = await close_entity(obj_db)
    elif rem_obj_in == rem_obj_db:
        obj_in = await close_entity(obj_in)
        obj_db = await close_entity(obj_db)
    else:
        obj_db.invested_amount += rem_obj_in
        obj_in = await close_entity(obj_in)
    return obj_in, obj_db


async def perform_investment(
    obj_in: InvestmentBaseModel,
    model_db: Type[Union[Donation, CharityProject]],
    session: AsyncSession
) -> InvestmentBaseModel:
    source_db_all = await session.execute(
        select(model_db).where(
            model_db.fully_invested == False  # noqa: E712
        ).order_by(model_db.create_date)
    )
    source_db_all = source_db_all.scalars().all()
    for source_db in source_db_all:
        obj_in, source_db = await distribution(
            obj_in, source_db
        )
        session.add(obj_in)
        session.add(source_db)
    await session.commit()
    await session.refresh(obj_in)
    return obj_in


async def create_new_object(
    obj_in,
    model,
    session: AsyncSession,
    user: Optional[User] = None,
    need_for_commit: Optional[bool] = True
) -> InvestmentBaseModel:
    obj_in_data = obj_in.dict()
    if obj_in_data.get('name') is not None:
        await vld.check_charity_project_name_duplicate(
            obj_in_data['name'], session
        )
    if user is not None:
        obj_in_data['user_id'] = user.id
    db_obj = model(**obj_in_data)
    if not need_for_commit and model is CharityProject:
        db_obj.invested_amount = 0
        db_obj.fully_invested = False
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    model_in = Donation if model is CharityProject else CharityProject
    return await perform_investment(
        obj_in=db_obj,
        model_db=model_in,
        session=session
    )


async def update_object(
    charity_project,
    obj_in: CharityProjectUpdate,
    session: AsyncSession,
) -> CharityProjectDB:
    await vld.check_charity_project_is_open(charity_project)
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
    return await charity_project_crud.update(charity_project, session)
