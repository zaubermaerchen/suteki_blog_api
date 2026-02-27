from datetime import date

from sqlalchemy import and_, desc, func, or_, select
from sqlalchemy.dialects.mysql import match
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import label

import api.models.entry as models


async def get(db: AsyncSession, entry_id: int) -> models.Entry | None:
    statement = select(models.Entry).where(models.Entry.id == entry_id)
    result = await db.execute(statement)
    return result.scalar()


async def search(
    db: AsyncSession,
    query: str,
    from_date: date | None,
    to_date: date | None,
    authors: list[str],
    limit: int,
    offset: int,
) -> tuple[list[tuple[models.Entry, float]], int]:
    # 検索条件設定
    where = or_(
        match(models.Entry.title, against=query).in_boolean_mode(),
        match(models.Entry.text, against=query).in_boolean_mode(),
        match(models.Entry.translation_text, against=query).in_boolean_mode(),
    )
    if from_date is not None:
        where = and_(where, models.Entry.date >= from_date)
    if to_date is not None:
        where = and_(where, models.Entry.date <= to_date)
    if len(authors) > 0:
        where = and_(
            where,
            match(models.Entry.authors, against=" OR ".join(authors)).in_boolean_mode(),
        )

    # 総件数取得
    statement = select(func.count(models.Entry.id).label("total")).where(where)
    result = await db.execute(statement)
    item = result.first()
    total: int = 0 if item is None else item[0]
    if total <= offset:
        return [], total

    # 対象位置のデータ取得
    score_label = label(
        "score",
        match(models.Entry.title, against=query).in_boolean_mode()
        + match(models.Entry.text, against=query).in_boolean_mode()
        + match(models.Entry.translation_text, against=query).in_boolean_mode(),
    )
    statement = (
        select(models.Entry, score_label)
        .where(where)
        .limit(limit)
        .offset(offset)
        .order_by(desc("score"))
    )
    result = await db.execute(statement)

    return [(item[0], item[1]) for item in result.fetchall()], total
