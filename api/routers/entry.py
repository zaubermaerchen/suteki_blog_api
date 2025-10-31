from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

import api.crud.entry as crud
import api.schemas.entry as schema
from api.database import get_session as get_database_session

router = APIRouter(
    prefix="/entry",
    tags=["entry"],
)


@router.get(
    "/search",
    response_model=schema.SearchEntryResponse,
    operation_id="search_entry",
    summary="日記検索",
)
async def search(
    query: str,
    from_date: date | None = None,
    to_date: date | None = None,
    authors: list[str] = Query([]),
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_database_session),
):
    [entries, count] = await crud.search(
        db,
        query=query,
        authors=authors,
        from_date=from_date,
        to_date=to_date,
        limit=limit,
        offset=offset,
    )
    return {
        "results": [
            schema.SearchResultEntry.from_model_and_score(*entry) for entry in entries
        ],
        "count": count,
    }


@router.get(
    "/{entry_id}",
    response_model=schema.GetEntryResponse,
    operation_id="get_entry",
    summary="日記詳細取得",
)
async def get(entry_id: int, db: AsyncSession = Depends(get_database_session)):
    entry = await crud.get(db, entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="entry is not found")
    return entry
