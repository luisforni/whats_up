from fastapi import APIRouter, HTTPException, Depends
from app.auth.schemas import UserCreate, UserLogin, UserResponse
from app.database import get_db
from sqlalchemy.orm import Session
from app.auth.models import User
from app.auth.utils import hash_password, verify_password

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return {"id": db_user.id, "email": db_user.email}

@router.get("/nearby")
def get_nearby_users(user_id: int, latitude: float, longitude: float, radius: int, db: Session = Depends(get_db)):
    # Obtiene todos los usuarios registrados (excepto el usuario actual)
    users = db.query(User).filter(User.id != user_id).all()

    # Lista de usuarios cercanos
    nearby_users = []

    # Ubicación del usuario actual
    user_location = (latitude, longitude)

    # Simula que cada usuario tiene latitud y longitud
    for user in users:
        # TODO: Reemplazar con datos reales de ubicación del usuario (lat, lon)
        user_latitude = getattr(user, "latitude", None)
        user_longitude = getattr(user, "longitude", None)

        if user_latitude is None or user_longitude is None:
            continue

        # Calcular la distancia entre el usuario actual y el usuario en la base de datos
        user_distance = geodesic(user_location, (user_latitude, user_longitude)).km

        # Agregar a la lista si está dentro del radio
        if user_distance <= radius:
            nearby_users.append({"email": user.email, "distance": round(user_distance, 2)})

    return nearby_users