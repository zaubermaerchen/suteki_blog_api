from sqlalchemy import Column, DateTime, Index, Integer, Text
from sqlalchemy.dialects.mysql import LONGTEXT

from api.models.base import Base


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
