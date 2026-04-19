from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import News
from schemas import NewsCreate, NewsUpdate, NewsOut

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("", response_model=list[NewsOut])
def list_news(db: Session = Depends(get_db)):
    return db.query(News).order_by(News.created_at.desc()).all()


@router.get("/{news_id}", response_model=NewsOut)
def get_news(news_id: int, db: Session = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="교회 소식을 찾을 수 없습니다")
    return news


@router.post("", response_model=NewsOut, status_code=201)
def create_news(data: NewsCreate, db: Session = Depends(get_db)):
    news = News(**data.model_dump())
    db.add(news)
    db.commit()
    db.refresh(news)
    return news


@router.put("/{news_id}", response_model=NewsOut)
def update_news(news_id: int, data: NewsUpdate, db: Session = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="교회 소식을 찾을 수 없습니다")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(news, key, value)
    db.commit()
    db.refresh(news)
    return news


@router.delete("/{news_id}", status_code=204)
def delete_news(news_id: int, db: Session = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="교회 소식을 찾을 수 없습니다")
    db.delete(news)
    db.commit()
