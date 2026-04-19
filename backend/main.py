import os
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

load_dotenv()

from routers import notices, news, gallery

APP_ENV = os.getenv("APP_ENV", "production")

app = FastAPI(
    title="하늘의 빛 교회 API",
    docs_url="/docs" if APP_ENV == "development" else None,
    redoc_url="/redoc" if APP_ENV == "development" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000, https://lightofsky.org"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def admin_guard(request: Request, call_next):
    if request.url.path.startswith("/admin"):
        if APP_ENV != "development":
            return Response(status_code=404)
    return await call_next(request)


app.include_router(notices.router)
app.include_router(news.router)
app.include_router(gallery.router)

uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

admin_dir = os.path.join(os.path.dirname(__file__), "..", "admin")
if os.path.isdir(admin_dir):
    app.mount("/admin", StaticFiles(directory=admin_dir, html=True), name="admin")


@app.get("/health")
def health():
    return {"status": "ok", "env": APP_ENV}
