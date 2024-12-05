from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Tweet(BaseModel):
    id: Optional[int] = None
    user_id: int  # ID del usuario que publicó el tweet
    content: str  # Contenido del tweet
    created_at: Optional[datetime] = None  # Fecha y hora de creación, opcional
    updated_at: Optional[datetime] = None  # Fecha y hora de actualización, opcional
