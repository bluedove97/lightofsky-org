from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Notice
from schemas import NoticeCreate, NoticeUpdate, NoticeOut, NoticeListOut

router = APIRouter(prefix="/api/notices", tags=["notices"])


@router.get("", response_model=NoticeListOut)
def list_notices(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    total = db.query(func.count(Notice.id)).scalar()
    items = (
        db.query(Notice)
        .order_by(Notice.is_pinned.desc(), Notice.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return NoticeListOut(items=items, total=total, page=page, limit=limit)


@router.get("/{notice_id}", response_model=NoticeOut)
def get_notice(notice_id: int, db: Session = Depends(get_db)):
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise HTTPException(status_code=404, detail="공지사항을 찾을 수 없습니다")
    return notice


@router.post("", response_model=NoticeOut, status_code=201)
def create_notice(data: NoticeCreate, db: Session = Depends(get_db)):
    notice = Notice(**data.model_dump())
    db.add(notice)
    db.commit()
    db.refresh(notice)
    return notice


@router.put("/{notice_id}", response_model=NoticeOut)
def update_notice(notice_id: int, data: NoticeUpdate, db: Session = Depends(get_db)):
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise HTTPException(status_code=404, detail="공지사항을 찾을 수 없습니다")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(notice, key, value)
    db.commit()
    db.refresh(notice)
    return notice


@router.delete("/{notice_id}", status_code=204)
def delete_notice(notice_id: int, db: Session = Depends(get_db)):
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise HTTPException(status_code=404, detail="공지사항을 찾을 수 없습니다")
    db.delete(notice)
    db.commit()
