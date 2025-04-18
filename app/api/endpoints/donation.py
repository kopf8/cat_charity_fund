from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import app.services.investment_func as f
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User, Donation
from app.schemas.donation import (DonationCreate, DonationFullDB,
                                  DonationShortDB)

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
    return await f.create_new_object(
        donation, Donation, session, user, need_for_commit=False
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
