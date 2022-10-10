# -*- coding: utf-8 -*-

from datetime import date
from typing import Optional, List, Tuple
from sqlalchemy import select, func, or_, and_, desc
from sqlalchemy.dialects.mysql import match
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import label
import api.models.entry as model

async def get(db: AsyncSession, entry_id: int) -> Optional[model.Entity]:
    statement = select(model.Entity).where(model.Entity.id==entry_id)
    result = await db.execute(statement)
    return result.scalar()

async def search(db: AsyncSession, query: str, from_date: Optional[date], to_date: Optional[date], authors: List[str], limit: int, offset: int) -> Tuple[List[Tuple[model.Entity, float]], int]:
    # 検索条件設定
    where = or_(
        match(model.Entity.title, against=query).in_boolean_mode(),
        match(model.Entity.text, against=query).in_boolean_mode(),
        match(model.Entity.translation_text, against=query).in_boolean_mode()
    )
    if from_date is not None:
        where = and_(where, model.Entity.date >= from_date)
    if to_date is not None:
        where = and_(where, model.Entity.date <= to_date)
    if len(authors) > 0:
        where = and_(where, match(model.Entity.authors, against=" OR ".join(authors)).in_boolean_mode())

    # 総件数取得
    statement = select(func.count(model.Entity.id).label("total")).where(where)
    result = await db.execute(statement)
    total = result.first()[0]
    if total <= offset:
        return [[], total]

    # 対象位置のデータ取得
    score_label = label('score', match(model.Entity.title, against=query).in_boolean_mode() + match(model.Entity.text, against=query).in_boolean_mode() + match(model.Entity.translation_text, against=query).in_boolean_mode())
    statement = select(model.Entity, score_label).where(where).limit(limit).offset(offset).order_by(desc('score'))
    result = await db.execute(statement)

    return [result.all(), total];
