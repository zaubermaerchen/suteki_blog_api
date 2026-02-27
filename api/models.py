from sqlalchemy import Column, Date, DateTime, Index, Integer, String, Text
from sqlalchemy.dialects.mysql import LONGTEXT

from api.database import Base


class Author(Base):
    __tablename__ = "author"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_bin",
        "mysql_engine": "Mroonga",
        "comment": 'default_tokenizer "TokenDelimit"',
    }

    name = Column(String(255), primary_key=True)


class Comment(Base):
    __tablename__ = "comment"
    __table_args__ = (
        Index("name", "name", mysql_prefix="FULLTEXT", mariadb_prefix="FULLTEXT"),
        Index("text", "text", mysql_prefix="FULLTEXT", mariadb_prefix="FULLTEXT"),
        {
            "mysql_charset": "utf8mb4",
            "mysql_engine": "Mroonga",
        },
    )

    id = Column(Integer, primary_key=True)
    entry_id = Column(Integer)
    name = Column(Text)
    date = Column(DateTime)
    url = Column(Text)
    text = Column(LONGTEXT)


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
