from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.posts.models import Post
from app.posts.schemas import PostCreate, PostResponse
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads/"  # Directorio para almacenar archivos multimedia
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=PostResponse, status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post  # Devuelve directamente el objeto creado

@router.post("/posts/upload", response_model=dict)
def upload_file(user_id: int, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_path": file_path}

@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()

@router.get("/posts/{user_id}", response_model=list[PostResponse])
def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    return db.query(Post).filter(Post.user_id == user_id).all()
