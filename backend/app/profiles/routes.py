from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.profiles.models import Profile
from app.profiles.schemas import ProfileCreate, ProfileResponse

router = APIRouter()

# Crear perfil
@router.post("/", response_model=ProfileResponse, status_code=201)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    db_profile = Profile(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

# Obtener perfil por user_id
@router.get("/{user_id}", response_model=ProfileResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return profile

# Actualizar perfil
@router.put("/{user_id}", response_model=ProfileResponse)
def update_profile(user_id: int, profile: ProfileCreate, db: Session = Depends(get_db)):
    db_profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    # Actualizar los campos del perfil
    for key, value in profile.dict().items():
        setattr(db_profile, key, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

# Verificar si existe un perfil
@router.get("/{user_id}/exists", response_model=bool)
def check_profile_exists(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    return profile is not None
