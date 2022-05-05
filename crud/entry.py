# -*- coding: utf-8 -*-

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import models.entry as model

async def get(db: AsyncSession, entry_id: int) -> Optional[model.Entity]:
    statement = select(model.Entity).where(model.Entity.id==entry_id)
    result = await db.execute(statement)
    return result.scalar()
