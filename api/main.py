# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import entry
from api.config import get_settings

settings = get_settings()

app = FastAPI(
    title="suteki_blog_api",
    description="WHOLE SWEET LIFE search API",
    debug=settings.debug
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins.split(",") if len(settings.cors_allow_origins) > 0 else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(entry.router)