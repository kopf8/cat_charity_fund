from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.crud.charity_project import charity_project_crud
from app.schemas.donation import (
    DonationCreate, DonationShortDB, DonationFullDB
)
from app.models import User, CharityProject, InvestmentBaseModel

from app.services.investment_func import perform_investment


router = APIRouter()


@router.post(
    '/',
    response_model=DonationShortDB,
    response_model_exclude_none=True
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """For registered users"""
    new_donation = await donation_crud.create(
        donation, session, user, need_for_commit=False
    )
    return await perform_investment(
        obj_in=new_donation,
        model_db=CharityProject,
        session=session,
    )


@router.get(
    '/',
    response_model=list[DonationFullDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """For superusers only"""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationShortDB],
    response_model_exclude_none=True,
    response_model_exclude={'user_id'}
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    return await donation_crud.get_user_donations(
        session=session,
        user=user
    )
