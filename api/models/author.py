from sqlalchemy import Column, String

from api.models.base import Base


class Author(Base):
    __tablename__ = "author"
    __table_args__ = {
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_bin",
        "mysql_engine": "Mroonga",
        "comment": 'default_tokenizer "TokenDelimit"',
    }

    name = Column(String(255), primary_key=True)
