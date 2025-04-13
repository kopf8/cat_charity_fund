from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Messages
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def get_project_or_404(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=Messages.PROJECT_NOT_FOUND
        )
    return charity_project
