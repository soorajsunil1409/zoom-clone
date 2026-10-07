from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import models
from .database import Base, engine
from .routers.meetings import router as meetings_router
from .routers.participants import router as participants_router
from .websocket.meeting_socket import router as websocket_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Zoom Clone API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(meetings_router)
app.include_router(participants_router)
app.include_router(websocket_router)


@app.get("/health")
def health():
    return {"status": "ok"}