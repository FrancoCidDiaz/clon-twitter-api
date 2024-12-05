from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from config.db import meta, engine
from datetime import datetime


tweets = Table(
    "tweets", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),  # Clave foránea a users
    Column("content", String(280), nullable=False),  # Limita el contenido a 280 caracteres
    Column("created_at", DateTime, default=datetime.now()),
    Column("updated_at", DateTime, onupdate=datetime.now())
)

meta.create_all(engine)