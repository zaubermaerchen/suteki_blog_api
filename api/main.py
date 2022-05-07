# -*- coding: utf-8 -*-
from fastapi import FastAPI
from api.routers import entry

app = FastAPI(
    title="suteki_blog_api",
    description="WHOLE SWEET LIFE data API"
)
app.include_router(entry.router)