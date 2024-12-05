from sqlalchemy import Table, Column, Integer, String
from config.db import meta, engine

# Definición de la tabla 'users'
users = Table(
    "users", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(25)),
    Column("email", String(255)),
    Column("password", String(255))
)

# Creación de la tabla en la base de datos
meta.create_all(engine)
