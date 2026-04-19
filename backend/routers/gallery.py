import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from models import Gallery
from schemas import GalleryOut

router = APIRouter(prefix="/api/gallery", tags=["gallery"])

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


@router.get("", response_model=list[GalleryOut])
def list_gallery(category: str = "all", db: Session = Depends(get_db)):
    query = db.query(Gallery).order_by(Gallery.created_at.desc())
    if category != "all":
        query = query.filter(Gallery.category == category)
    return query.all()


@router.post("", response_model=GalleryOut, status_code=201)
async def upload_gallery(
    title: str = Form(...),
    category: str = Form("all"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="허용되지 않는 파일 형식입니다")

    filename = f"{uuid.uuid4()}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)

    image_url = f"/uploads/{filename}"
    gallery = Gallery(title=title, image_url=image_url, category=category)
    db.add(gallery)
    db.commit()
    db.refresh(gallery)
    return gallery


@router.delete("/{gallery_id}", status_code=204)
def delete_gallery(gallery_id: int, db: Session = Depends(get_db)):
    gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()
    if not gallery:
        raise HTTPException(status_code=404, detail="이미지를 찾을 수 없습니다")

    filepath = os.path.join(UPLOAD_DIR, os.path.basename(gallery.image_url))
    if os.path.exists(filepath):
        os.remove(filepath)

    db.delete(gallery)
    db.commit()
