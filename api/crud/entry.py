from datetime import date

from sqlalchemy import and_, desc, func, or_, select
from sqlalchemy.dialects.mysql import match
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import label

from api.models import Entry as EntryModel


async def get(db: AsyncSession, entry_id: int) -> EntryModel | None:
    statement = select(EntryModel).where(EntryModel.id == entry_id)
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
) -> tuple[list[tuple[EntryModel, float]], int]:
    # 検索条件設定
    where = or_(
        match(EntryModel.title, against=query).in_boolean_mode(),
        match(EntryModel.text, against=query).in_boolean_mode(),
        match(EntryModel.translation_text, against=query).in_boolean_mode(),
    )
    if from_date is not None:
        where = and_(where, EntryModel.date >= from_date)
    if to_date is not None:
        where = and_(where, EntryModel.date <= to_date)
    if len(authors) > 0:
        where = and_(
            where,
            match(EntryModel.authors, against=" OR ".join(authors)).in_boolean_mode(),
        )

    # 総件数取得
    statement = select(func.count(EntryModel.id).label("total")).where(where)
    result = await db.execute(statement)
    item = result.first()
    total: int = 0 if item is None else item[0]
    if total <= offset:
        return [], total

    # 対象位置のデータ取得
    score_label = label(
        "score",
        match(EntryModel.title, against=query).in_boolean_mode()
        + match(EntryModel.text, against=query).in_boolean_mode()
        + match(EntryModel.translation_text, against=query).in_boolean_mode(),
    )
    statement = (
        select(EntryModel, score_label)
        .where(where)
        .limit(limit)
        .offset(offset)
        .order_by(desc("score"))
    )
    result = await db.execute(statement)

    return [(item[0], item[1]) for item in result.fetchall()], total
