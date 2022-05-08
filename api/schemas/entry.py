# -*- coding: utf-8 -*-
from datetime import date as date_type
from pydantic import BaseModel, Field, validator
from typing import List, Type

class GetEntryResponse(BaseModel):
    id: int = Field(name="🆔")
    date: date_type = Field(name="URL", example="2022-01-01")
    title: str = Field(name="日記タイトル")
    text: str = Field(name="日記本文")
    translation_text: str = Field(name="日記翻訳文")
    url: str = Field(name="URL", example="https://example.com")
    authors: List[str] = Field(name="投稿者")

    class Config:
        orm_mode = True
    
    @validator('authors', pre=True)
    def split_authors(cls, v):
        if isinstance(v, str):
            return v.split() if len(v) > 0 else []
        return v

class SearchResultEntry(BaseModel):
    id: int = Field(name="🆔")
    date: date_type = Field(name="URL", example="2022-01-01")
    title: str = Field(name="日記タイトル")
    text: str = Field(name="日記本文")
    url: str = Field(name="URL", example="https://example.com")
    authors: List[str] = Field(name="投稿者")
    score: float = Field(0, name="検索スコア")

    class Config:
        orm_mode = True

    @validator('text', pre=True)
    def summary_text(cls, v):
        if isinstance(v, str):
            return v.replace("\r\n", "")[:100]
        return v
    
    @validator('authors', pre=True)
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
    results: List[SearchResultEntry] = Field([], name="日記リスト")
    count: int = Field(0, name="総件数")