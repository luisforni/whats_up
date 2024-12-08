from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.auth.routes import router as auth_router
from app.profiles.routes import router as profiles_router
from app.posts.routes import router as posts_router
from app.chat.routes import router as chat_router

# Crear las tablas de la base de datos al iniciar la app
Base.metadata.create_all(bind=engine)

# Instancia de FastAPI
app = FastAPI(
    title="Chat and Posts App",
    description="API para manejar autenticación, perfiles, publicaciones y chat",
    version="1.0.0",
)

# Middleware CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto a una lista específica de dominios en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(profiles_router, prefix="/api/profiles", tags=["Profiles"])
app.include_router(posts_router, prefix="/api/posts", tags=["Posts"])
app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])

# Raíz
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Chat y Publicaciones"}
