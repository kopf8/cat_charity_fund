from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_invested,
                                check_charity_project_is_open,
                                check_charity_project_name_duplicate,
                                check_new_full_amount)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.get_project_or_404 import get_project_or_404
from app.services.investment_func import perform_investment

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """For superusers only"""
    await check_charity_project_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    return await perform_investment(
        obj_in=new_project,
        model_db=Donation,
        session=session
    )


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """For any user"""
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """For superuser only"""
    charity_project = await get_project_or_404(project_id, session)
    await check_charity_project_is_open(project_id, session)
    if obj_in.full_amount:
        check_new_full_amount(
            charity_project.invested_amount,
            obj_in.full_amount
        )
    if obj_in.name:
        await check_charity_project_name_duplicate(obj_in.name, session)
    return await charity_project_crud.update(charity_project, obj_in, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """For superusers only"""
    charity_project = await get_project_or_404(
        project_id, session
    )
    await check_charity_project_is_open(project_id, session)
    await check_charity_project_invested(
        project_id, session
    )
    return await charity_project_crud.remove(
        charity_project, session
    )
