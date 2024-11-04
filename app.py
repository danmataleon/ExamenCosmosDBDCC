from fastapi import FastAPI, HTTPException, Query, Path 
from typing import List, Optional
from database import users_container, projects_container
from models import usuario, proyecto
from azure.cosmos import exceptions
from datetime import datetime

app = FastAPI(title='API de Gestion de Usuarios y Proyectos')


@app.get("/")
def home():
    return "Hola Mundo"

# USUARIOS
# Listar usuarios
@app.get("/usuarios/", response_model=List[usuario])
def list_usuario():
    query = "SELECT * FROM c WHERE 1=1"
    items = list(users_container.query_items(query=query, enable_cross_partition_query=True))
    return items

# crear usuario
@app.post("/usuarios/", response_model=usuario, status_code=201)
def create_usuario(usuario: usuario):
    try:
        container.create_item(body=usuario.dict())
        return usuario
    except exceptions.CosmosResourceExistsError:
        raise HTTPException(status_code=400, detail= "El usuario con este id ya existe!!")
    except exceptions.CosmosHTTPResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# actualizar usuario
@app.put("/usuarios/{usuario_id}", response_model=usuario)
def update_usuario(usuario_id:str, updated_usuario: usuario):
    # buscar el item (retorna un tipo diccionario):
    existing_usuario = users_container.read_item(item=usuario_id, partition_key=usuario_id)
    existing_usuario.update(updated_usuario.dict(exclude_unset=True)) # recupera solo los campos que han sido proporcionados
    users_container.replace_item(item = usuario_id, body=existing_usuario)
    return existing_usuario

#eliminar usuario
@app.delete("/usuarios/{usuario_id}", status_code=204)
def delete_usuario(usuario_id:str):
    try:
        users_container.delete_item(item=usuario_id, partition_key=usuario_id)
        return
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Usuario a eliminar no encontrado.")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))



# PROYECTOS
# Listar proyectos
@app.get("/proyectos/", response_model=List[proyecto])
def list_proyecto():
    query = "SELECT * FROM c WHERE 1=1"
    items = list(projects_container.query_items(query=query, enable_cross_partition_query=True))
    return items

# crear proyecto
@app.post("/proyectos/", response_model=proyecto, status_code=201)
def create_proyecto(proyecto: proyecto):
    try:
        projects_container.create_item(body=proyecto.dict())
        return proyecto
    except exceptions.CosmosResourceExistsError:
        raise HTTPException(status_code=400, detail= "El proyecto con este id ya existe!!")
    except exceptions.CosmosHTTPResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# actualizar proyecto
@app.put("/proyectos/{proyecto_id}", response_model=proyecto)
def update_proyecto(proyecto_id:str, updated_proyecto: proyecto):
    # buscar el item (retorna un tipo diccionario):
    existing_proyecto = projects_container.read_item(item=proyecto_id, partition_key=proyecto_id)
    existing_proyecto.update(updated_proyecto.dict(exclude_unset=True)) # recupera solo los campos que han sido proporcionados
    projects_container.replace_item(item = proyecto_id, body=existing_proyecto)
    return existing_proyecto

#eliminar proyecto
@app.delete("/proyectos/{proyecto_id}", status_code=204)
def delete_proyecto(proyecto_id:str):
    try:
        projects_container.delete_item(item=proyecto_id, partition_key=proyecto_id)
        return
    except exceptions.CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Proyecto a eliminar no encontrado.")
    except exceptions.CosmosHttpResponseError as e:
        raise HTTPException(status_code=400, detail=str(e))
