# -*- coding: utf-8 -*-
from datetime import date as date_type
from pydantic import BaseModel, Field, validator
from typing import List

class EntryResponse(BaseModel):
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
            return v.split(" ")
        return v