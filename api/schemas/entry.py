from datetime import date as date_type

from pydantic import BaseModel, Field, field_validator


class GetEntryResponse(BaseModel):
    id: int = Field(title="🆔")
    date: date_type = Field(title="URL", examples=["2022-01-01"])
    title: str = Field(title="日記タイトル")
    text: str = Field(title="日記本文")
    translation_text: str = Field(title="日記翻訳文")
    url: str = Field(title="URL", examples=["https://example.com"])
    authors: list[str] = Field(title="投稿者")

    class Config:
        from_attributes = True

    @field_validator("authors", mode="before")
    def split_authors(cls, v):
        if isinstance(v, str):
            return v.split() if len(v) > 0 else []
        return v


class SearchResultEntry(BaseModel):
    id: int = Field(title="🆔")
    date: date_type = Field(title="URL", examples=["2022-01-01"])
    title: str = Field(title="日記タイトル")
    text: str = Field(title="日記本文")
    url: str = Field(title="URL", examples=["https://example.com"])
    authors: list[str] = Field(title="投稿者")
    score: float = Field(0, title="検索スコア")

    class Config:
        from_attributes = True

    @field_validator("text", mode="before")
    def summary_text(cls, v):
        if isinstance(v, str):
            return v.replace("\r\n", "")[:100]
        return v

    @field_validator("authors", mode="before")
    def split_authors(cls, v):
        if isinstance(v, str):
            return v.split() if len(v) > 0 else []
        return v

    @classmethod
    def from_orm_and_score(cls, model, score: float):
        schema = cls.from_orm(model)
        schema.score = score
        return schema


class SearchEntryResponse(BaseModel):
    results: list[SearchResultEntry] = Field([], title="日記リスト")
    count: int = Field(0, title="総件数")
