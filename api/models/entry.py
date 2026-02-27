from sqlalchemy import Column, Date, Index, Integer, Text
from sqlalchemy.dialects.mysql import LONGTEXT

from api.models.base import Base


class Entry(Base):
    __tablename__ = "entry"
    __table_args__ = (
        Index("idx_title", "title", mysql_prefix="FULLTEXT", mariadb_prefix="FULLTEXT"),
        Index("idx_text", "text", mysql_prefix="FULLTEXT", mariadb_prefix="FULLTEXT"),
        Index(
            "idx_translation_text",
            "translation_text",
            mysql_prefix="FULLTEXT",
            mariadb_prefix="FULLTEXT",
        ),
        Index(
            "idx_authors",
            "authors",
            mysql_prefix="FULLTEXT",
            mariadb_prefix="FULLTEXT",
        ),
        {
            "mysql_charset": "utf8mb4",
            "mysql_engine": "Mroonga",
        },
    )

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    title = Column(Text)
    text = Column(LONGTEXT)
    translation_text = Column(LONGTEXT)
    url = Column(Text)
    authors = Column(Text, comment='flags "COLUMN_VECTOR", type "author"')
