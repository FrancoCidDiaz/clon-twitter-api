from sqlalchemy import Table, Column, Integer, DateTime, ForeignKey
from config.db import meta, engine
from datetime import datetime


likes = Table(
    "likes", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("tweet_id", Integer, ForeignKey("tweets.id"), nullable=False),  # Clave foránea a tweets
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),  # Clave foránea a users
    Column("created_at", DateTime, default=datetime.utcnow)
)

meta.create_all(engine)