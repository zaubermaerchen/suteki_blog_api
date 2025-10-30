from sqlalchemy import Column, Date, Index, Integer, Text
from sqlalchemy.dialects.mysql import LONGTEXT

from api.database import Base


class Entry(Base):
    __tablename__ = "entry"
    __table_args__ = {"mysql_charset": "utf8mb4", "mysql_engine": "Mroonga"}

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    title = Column(Text)
    text = Column(LONGTEXT)
    translation_text = Column(LONGTEXT)
    url = Column(Text)
    authors = Column(Text, comment='flags "COLUMN_VECTOR", type "author"')


Index("idx_title", Entry.title, mysql_prefix="FULLTEXT", mariadb_prefix="FULLTEXT")
Index("idx_text", Entry.text, mysql_prefix="FULLTEXT", mariadb_prefix="FULLTEXT")
Index(
    "idx_translation_text",
    Entry.translation_text,
    mysql_prefix="FULLTEXT",
    mariadb_prefix="FULLTEXT",
)
Index("idx_authors", Entry.authors, mysql_prefix="FULLTEXT", mariadb_prefix="FULLTEXT")
