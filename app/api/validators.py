from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Messages
from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_charity_project_name_duplicate(
        project_name: str,
        session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get_charity_project_by_name(
        project_name, session
    )
    if charity_project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=Messages.PROJECT_NAME_OCCUPIED
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=Messages.PROJECT_NOT_FOUND
        )
    return charity_project


async def check_charity_project_is_open(
        charity_project_id: int,
        session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=Messages.PROJECT_CLOSED
        )


async def check_charity_project_invested(
        charity_project_id: int,
        session: AsyncSession
) -> None:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=Messages.PROJECT_INVESTED
        )


def check_new_full_amount(
        current_amount: int,
        new_amount: int
) -> None:
    if new_amount < current_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=Messages.PROJECT_AMOUNTS_ERROR
        )
