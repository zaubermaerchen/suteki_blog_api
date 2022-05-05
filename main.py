# -*- coding: utf-8 -*-
from fastapi import FastAPI
from routers import entry

app = FastAPI()
app.include_router(entry.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}