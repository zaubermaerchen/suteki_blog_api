# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session as get_database_session
import schemas.entry as schema
import crud.entry as crud

router = APIRouter(
    prefix="/entry",
    tags=["entry"],
)

@router.get("/{entry_id}", response_model=schema.EntryResponse, operation_id="get_entry", summary="日記詳細取得")
async def get(entry_id: int, db: AsyncSession = Depends(get_database_session)):
    entry = await crud.get(db, entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="entry is not found")
    return entry
