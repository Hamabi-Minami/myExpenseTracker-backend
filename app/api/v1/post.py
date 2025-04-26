from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.dependencies import get_db, get_current_user
from app.models import User
from app.models.article import Article
from app.schemas.post import PostResponse, PostCreate

router = APIRouter()


@router.get("/")
async def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(Article).all()

    response = []
    for post in posts:
        response.append({
            "id": post.id,
            "title": post.title,
            "content": post.content[:120],
            "author": {
                "username": post.author.username if post.author else "Unknown"
            },
            "created_at": post.created_at.strftime("%Y-%m-%d %H:%M"),
            "likes": post.likes if hasattr(post, "likes") else 0,
            "comments": post.comments if hasattr(post, "comments") else 0,
            "cover_url": post.cover_url if hasattr(post, "cover_url") else "https://via.placeholder.com/150"
        })

    return response


@router.get("/me", response_model=List[PostResponse])
async def get_my_posts(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    posts = db.query(Article).filter(Article.author_id == current_user.id).all()

    response = []
    for post in posts:
        response.append({
            "id": post.id,
            "title": post.title,
            "content": post.content[:120],
            "author": {
                "username": current_user.username
            },
            "created_at": post.created_at.strftime("%Y-%m-%d %H:%M"),
            "likes": post.likes if hasattr(post, "likes") else 0,
            "comments": post.comments if hasattr(post, "comments") else [],
            "cover_url": post.cover_url if hasattr(post, "cover_url") else "https://via.placeholder.com/150"
        })

    return response


@router.get("/{post_id}")
async def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Article).filter(Article.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "created_at": post.created_at,
        "author": {
            "id": post.author.id,
            "username": post.author.username,
        } if post.author else None
    }


@router.post("/", response_model=PostResponse, status_code=201)
async def publish_post(
        post_data: PostCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    try:
        new_post = Article(
            title=post_data.title,
            content=post_data.content,
            author_id=current_user.id,
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        response = {
            "id": new_post.id,
            "title": new_post.title,
            "content": new_post.content[:120],
            "author": {
                "username": current_user.username
            },
            "created_at": new_post.created_at.strftime("%Y-%m-%d %H:%M"),
            "likes": new_post.likes if hasattr(new_post, "likes") else 0,
            "comments": new_post.comments if hasattr(new_post, "comments") else [],
            "cover_url": new_post.cover_url if hasattr(new_post, "cover_url") else "https://via.placeholder.com/150"
        }

        return response
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
