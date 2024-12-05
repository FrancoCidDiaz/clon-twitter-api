from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import logging

# Configuración de logging para SQLAlchemy
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = create_engine("mysql+pymysql://root:1234@localhost:3306/fastapidb")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

meta = MetaData()

conn = engine.connect()

