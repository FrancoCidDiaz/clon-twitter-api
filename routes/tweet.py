from fastapi import APIRouter, Response, HTTPException
from config.db import conn
from models.tweet import tweets
from schemas.tweet import Tweet
from datetime import datetime
from starlette.status import HTTP_200_OK


tweet = APIRouter()



@tweet.post('/tweets')
def create_tweet(tweet: Tweet):
    try:
        # Lógica para crear un nuevo tweet en la base de datos
        new_tweet = conn.execute(tweets.insert().values(
            user_id=tweet.user_id,
            content=tweet.content,
            created_at=datetime.now()
        ))
        conn.commit()
        tweet_id = new_tweet.inserted_primary_key[0]  # Asegúrate de que `inserted_primary_key` sea la forma correcta de obtener el ID

        # Devolver los datos completos del tweet recién creado
        return {
            "id": tweet_id,
            "user_id": tweet.user_id,
            "content": tweet.content,
            "created_at": datetime.now()
        }
    except Exception as e:
        print("Error al crear el tweet:", str(e))
        return {"error": "Error al crear el tweet", "details": str(e)}, 500
    

@tweet.get('/tweets/{user_id}')
def get_tweets_by_user(user_id : int):
    try:
        tweets_data = conn.execute(tweets.select().where(tweets.c.user_id == user_id)).fetchall()
        tweets_list = [
            {
                "id": tweet[0],
                "user_id": tweet[1],
                "content": tweet[2],
                "created_at": tweet[3],
                "updated_at": tweet[4]
            } for tweet in tweets_data
        ]

        return {"tweets": tweets_list}  # Retorna todos los tweets del usuario
    except Exception as e:
        # Maneja el error y proporciona detalles
        print("Error al obtener los tweets", str(e))  # Imprimir el error en consola para depuración
        return {"error": "Error al obtener los tweets", "details": str(e)}, 500  # Retorna un error 500
    

@tweet.delete('/tweets/{id}')
def delete_tweet(id: int):
     conn.execute(tweets.delete().where(tweets.c.id == id))
     conn.commit()
     return Response(status_code=HTTP_200_OK)



@tweet.put('/tweets/{id}')
def update_tweet(id: int, tweet: Tweet):
    try:
        print(f"Actualizando tweet con ID {id} y nuevo contenido: {tweet.content}")  # Agrega esto para depuración
        result = conn.execute(tweets.update().where(tweets.c.id == id).values(
            content=tweet.content,
            updated_at=datetime.now()
        ))

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Tweet no encontrado")

        conn.commit()
        return {"message": "Tweet actualizado exitosamente", "tweet": tweet}
    except Exception as e:
        print("Error al actualizar el tweet:", str(e))
        raise HTTPException(status_code=500, detail="Error al actualizar el tweet")