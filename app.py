from fastapi import FastAPI
from routes.user import user
from routes.tweet import tweet
from routes.like import like
import logging
from config.db import conn  # Asegúrate de que la conexión se esté importando correctamente
from fastapi.middleware.cors import CORSMiddleware

# Configuración de logging para SQLAlchemy
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Cambia esto por el origen correcto de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user)
app.include_router(tweet)
app.include_router(like)



