from sqlalchemy import Table, Column, Integer, String
from config.db import meta, engine



hashtags = Table(
    "hashtags", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), unique=True, nullable=False)  # Asegúrate de que las etiquetas sean únicas
)


meta.create_all(engine)