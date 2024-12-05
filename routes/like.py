from fastapi import APIRouter, Response, HTTPException
from config.db import conn
from models.like import likes  # Asegúrate de tener un modelo para likes
from schemas.like import Like  # Asegúrate de tener un esquema para likes
from datetime import datetime
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

like = APIRouter()

# Crear un like
@like.post('/likes', status_code=HTTP_201_CREATED)
def create_like(like: Like):
    try:
        # Lógica para crear un nuevo like en la base de datos
        new_like = conn.execute(likes.insert().values(
            user_id=like.user_id,
            tweet_id=like.tweet_id,
            created_at=datetime.now()  # Si quieres tener un campo de created_at
        ))
        conn.commit()
        like_id = new_like.inserted_primary_key[0]

        return {
            "id": like_id,
            "user_id": like.user_id,
            "tweet_id": like.tweet_id,
            "created_at": datetime.now()  # Asegúrate de que este valor sea correcto
        }
    except Exception as e:
        print("Error al crear el like:", str(e))
        raise HTTPException(status_code=500, detail="Error al crear el like")

# Obtener todos los likes para un tweet específico
@like.get('/likes/{tweet_id}')
def get_likes_by_tweet(tweet_id: int):
    try:
        likes_data = conn.execute(likes.select().where(likes.c.tweet_id == tweet_id)).fetchall()
        likes_list = [
            {
                "id": like[0],
                "user_id": like[1],
                "tweet_id": like[2],
                "created_at": like[3],
            } for like in likes_data
        ]

        return {"likes": likes_list}  # Retorna todos los likes del tweet
    except Exception as e:
        print("Error al obtener los likes:", str(e))
        raise HTTPException(status_code=500, detail="Error al obtener los likes")

# Eliminar un like
@like.delete('/likes/{id}', status_code=HTTP_204_NO_CONTENT)
def delete_like(id: int):
    try:
        # Verificar si el like existe
        result = conn.execute(likes.select().where(likes.c.id == id)).fetchone()
        
        if result is None:
            raise HTTPException(status_code=404, detail="Like no encontrado")

        # Eliminar el like
        conn.execute(likes.delete().where(likes.c.id == id))
        conn.commit()
    except Exception as e:
        print("Error al eliminar el like:", str(e))
        raise HTTPException(status_code=500, detail="Error al eliminar el like")

# Contar likes de un tweet
@like.get('/likes/count/{tweet_id}')
def count_likes(tweet_id: int):
    try:
        count_result = conn.execute(likes.select().where(likes.c.tweet_id == tweet_id)).fetchall()
        count = len(count_result)

        return {"tweet_id": tweet_id, "likes_count": count}
    except Exception as e:
        print("Error al contar likes:", str(e))
        raise HTTPException(status_code=500, detail="Error al contar likes")