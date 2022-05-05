# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Text, Date, Index
from sqlalchemy.dialects.mysql import LONGTEXT
from database import Base

class Entity(Base):
    __tablename__ = "entry"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_engine": "Mroonga"
    }

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    title = Column(Text)
    text = Column(LONGTEXT)
    translation_text = Column(LONGTEXT)
    url = Column(Text)
    authors = Column(Text, comment="flags \"COLUMN_VECTOR\", type \"author\"")

Index("idx_title", Entity.title, mysql_prefix="FULLTEXT", mariadb_prefix="FULLTEXT")
Index("idx_text", Entity.text, mysql_prefix="FULLTEXT", mariadb_prefix="FULLTEXT")
Index("idx_translation_text", Entity.translation_text, mysql_prefix="FULLTEXT", mariadb_prefix="FULLTEXT")
Index("idx_authors", Entity.authors, mysql_prefix="FULLTEXT", mariadb_prefix="FULLTEXT")
