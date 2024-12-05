from fastapi import APIRouter, Response, HTTPException
from config.db import conn
from models.user import users
from schemas.user import User, UserLogin
from cryptography.fernet import Fernet
from starlette.status import HTTP_200_OK
from passlib.context import CryptContext
import bcrypt




user = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

# Función para verificar si la contraseña ingresada es correcta
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



@user.get('/users', response_model=list[User])
def get_users():
    try:
        # Ejecuta la consulta y almacena los resultados
        users_list = conn.execute(users.select()).fetchall()

        # Verifica el tipo de resultado y su contenido
        print("Resultados de la consulta:", users_list)
        
        # Convierte cada fila a un diccionario
        if users_list:
            # Aquí se espera que users_list sea una lista de RowProxy
            result = []
            for row in users_list:
                result.append({
                    "id": row[0],        # Primer elemento es el id
                    "name": row[1],      # Segundo elemento es el nombre
                    "email": row[2],     # Tercer elemento es el email
                    "password": row[3]   # Cuarto elemento es la contraseña
                })  # Convierte cada fila a diccionario
            return result
        else:
            return [], 200  # Retorna una lista vacía si no hay usuarios
    except Exception as e:
        # Maneja el error y proporciona detalles
        print("Error al obtener usuarios:", str(e))  # Imprimir el error en consola para depuración
        return {"error": "Error al obtener usuarios", "details": str(e)}, 500


@user.get('/users/{id}')
def get_user(id: int):  # Cambia el tipo de id a int, ya que es más adecuado para un ID numérico
    try:
        # Ejecuta la consulta para obtener el usuario por ID
        user_data = conn.execute(users.select().where(users.c.id == id)).first()

        # Verifica si se encontró el usuario
        if user_data:
            # Convierte la fila a diccionario
            user_dict = {
                'id': user_data[0],
                'name': user_data[1],
                'email': user_data[2],
                'password': user_data[3]  # O quizás quieras encriptar este valor antes de retornarlo
            }
            return user_dict
        else:
            return {"error": "Usuario no encontrado"}, 404  # Retorna 404 si no se encuentra el usuario
    except Exception as e:
        # Maneja el error y proporciona detalles
        print("Error al obtener el usuario:", str(e))  # Imprimir el error en consola para depuración
        return {"error": "Error al obtener el usuario", "details": str(e)}, 500  # Retorna un error 500
    


@user.delete('/users/{id}')
def delete_user(id: int):
    conn.execute(users.delete().where(users.c.id == id))
    conn.commit()
    return Response(status_code=HTTP_200_OK)

@user.put('/users/{id}') 
def update_user(id: int, user: User):
    conn.execute(
    users.update()
    .where(users.c.id == id)
    .values(
        name=user.name, 
        email=user.email, 
        password=f.encrypt(user.password.encode("utf-8"))))
    conn.commit()
    return "updated"
  
@user.post('/login')
def login_user(user: UserLogin):
    try:
        user_data = conn.execute(users.select().where(users.c.email == user.email)).first()

        if not user_data:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        print("Contraseña ingresada:", user.password)
        print("Hash de contraseña en la base de datos:", user_data[3])  # Verifica este índice

        if verify_password(user.password, user_data[3]):
            print("Contraseña verificada correctamente.")
            print(user_data[0])

            return {"userId": user_data[0]}, 200
        else:
            print("Contraseña incorrecta, comparación fallida.")
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    except Exception as e:
        print("Error en el login:", str(e))
        raise HTTPException(status_code=500, detail="Error en el servidor")



@user.post('/register')
def create_user(user: User):
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password)  # Cambiado aquí
    }
    print("Conectado a la base de datos:", conn)
    result = conn.execute(users.insert().values(new_user))
    conn.commit()
    
    print("Nuevo usuario insertado con ID:", result.lastrowid)

    # Obtener el nuevo usuario insertado
    created_user = conn.execute(users.select().where(users.c.id == result.lastrowid)).first()
    print(created_user)

    # Convertir el resultado en un diccionario, omitiendo la contraseña
    return { "id": created_user.id, "name": created_user.name, "email": created_user.email }  # No retornes la contraseña
