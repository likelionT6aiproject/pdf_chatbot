from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.upload import router as upload_router
from routers.read import router as read_router
from routers.index import router as index_router

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(index_router, prefix="")
app.include_router(upload_router, prefix="/upload")
app.include_router(read_router, prefix="/read")
