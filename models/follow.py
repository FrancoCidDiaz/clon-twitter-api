from sqlalchemy import Table, Column, Integer, DateTime, ForeignKey, UniqueConstraint
from config.db import meta, engine
from datetime import datetime

follows = Table(
    "follows", meta,
    Column("follower_id", Integer, ForeignKey("users.id"), nullable=False),  # Clave foránea a users
    Column("followed_id", Integer, ForeignKey("users.id"), nullable=False),  # Clave foránea a users
    Column("created_at", DateTime, default=datetime.now()),
    # Asegúrate de que no haya duplicados
    UniqueConstraint("follower_id", "followed_id", name="uq_follower_followed")
)


meta.create_all(engine)
