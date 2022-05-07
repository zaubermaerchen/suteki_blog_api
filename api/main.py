# -*- coding: utf-8 -*-
from fastapi import FastAPI
from api.routers import entry
from api.config import get_settings

settings = get_settings()

app = FastAPI(
    title="suteki_blog_api",
    description="WHOLE SWEET LIFE data API",
    debug=settings.debug
)
app.include_router(entry.router)