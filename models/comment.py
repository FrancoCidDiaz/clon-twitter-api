from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from config.db import meta, engine
from datetime import datetime

comments = Table(
    "comments", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("tweet_id", Integer, ForeignKey("tweets.id"), nullable=False),  # Clave foránea a tweets
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),  # Clave foránea a users
    Column("content", String(280), nullable=False),  # Limita el contenido a 280 caracteres
    Column("created_at", DateTime, default=datetime.utcnow)
)
