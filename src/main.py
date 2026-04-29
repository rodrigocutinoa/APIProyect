from datetime import datetime, timezone
from typing import List, Optional

from bson import ObjectId
from fastapi import FastAPI, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .db import get_collection
from .models import (
    ProjectCreate,
    ProjectInDB,
    ProjectUpdate,
    TaskCreate,
    TaskInDB,
    TaskUpdate,
)

app = FastAPI(title="APIProyect", version="0.2.0")
app.mount("/ui", StaticFiles(directory="static", html=True), name="static")

PROJECT_COLLECTION = "projects"
TASK_COLLECTION = "tasks"


def parse_object_id(value: str, name: str = "id") -> ObjectId:
    try:
        return ObjectId(value)
    except Exception:
        raise HTTPException(status_code=400, detail=f"ID de {name} inválido")


def serialize_doc(doc: dict) -> dict:
    serialized = dict(doc)
    if "_id" in serialized:
        serialized["_id"] = str(serialized["_id"])
    if "project_id" in serialized and isinstance(serialized["project_id"], ObjectId):
        serialized["project_id"] = str(serialized["project_id"])
    return serialized


@app.get("/api/v1/projects", response_model=List[ProjectInDB])
async def list_projects(name: Optional[str] = Query(None, description="Buscar proyectos por nombre")):
    collection = await get_collection(PROJECT_COLLECTION)
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    cursor = collection.find(query)
    projects = []
    async for doc in cursor:
        projects.append(serialize_doc(doc))
    return projects


@app.post("/api/v1/projects", response_model=ProjectInDB)
async def create_project(project: ProjectCreate):
    collection = await get_collection(PROJECT_COLLECTION)
    doc = jsonable_encoder(project)
    now = datetime.now(timezone.utc)
    doc["created_at"] = now
    doc["updated_at"] = now
    result = await collection.insert_one(doc)
    created = await collection.find_one({"_id": result.inserted_id})
    if created is None:
        raise HTTPException(status_code=500, detail="No se pudo crear el proyecto")
    return JSONResponse(status_code=201, content=jsonable_encoder(serialize_doc(created)))


@app.get("/api/v1/projects/{project_id}", response_model=ProjectInDB)
async def get_project(project_id: str):
    collection = await get_collection(PROJECT_COLLECTION)
    doc = await collection.find_one({"_id": parse_object_id(project_id, "project")})
    if doc is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return serialize_doc(doc)


@app.put("/api/v1/projects/{project_id}", response_model=ProjectInDB)
async def update_project(project_id: str, project: ProjectUpdate):
    collection = await get_collection(PROJECT_COLLECTION)
    update_data = project.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se proporcionaron campos para actualizar")
    update_data["updated_at"] = datetime.now(timezone.utc)
    result = await collection.update_one({"_id": parse_object_id(project_id, "project")}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    doc = await collection.find_one({"_id": parse_object_id(project_id, "project")})
    return serialize_doc(doc)


@app.delete("/api/v1/projects/{project_id}")
async def delete_project(project_id: str):
    project_collection = await get_collection(PROJECT_COLLECTION)
    task_collection = await get_collection(TASK_COLLECTION)
    oid = parse_object_id(project_id, "project")
    result = await project_collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    await task_collection.delete_many({"project_id": oid})
    return {"deleted": True, "id": project_id}


@app.get("/api/v1/projects/{project_id}/tasks", response_model=List[TaskInDB])
async def list_project_tasks(project_id: str):
    collection = await get_collection(TASK_COLLECTION)
    query = {"project_id": parse_object_id(project_id, "project")}
    cursor = collection.find(query)
    tasks = []
    async for doc in cursor:
        tasks.append(serialize_doc(doc))
    return tasks


@app.get("/api/v1/tasks", response_model=List[TaskInDB])
async def list_tasks(
    project_id: Optional[str] = Query(None, description="Filtrar tareas por proyecto"),
    status: Optional[str] = Query(None, description="Filtrar tareas por estado"),
    title: Optional[str] = Query(None, description="Filtrar tareas por título"),
):
    collection = await get_collection(TASK_COLLECTION)
    query = {}
    if project_id:
        query["project_id"] = parse_object_id(project_id, "project")
    if status:
        query["status"] = status
    if title:
        query["title"] = {"$regex": title, "$options": "i"}
    cursor = collection.find(query)
    tasks = []
    async for doc in cursor:
        tasks.append(serialize_doc(doc))
    return tasks


@app.post("/api/v1/tasks", response_model=TaskInDB)
async def create_task(task: TaskCreate):
    project_collection = await get_collection(PROJECT_COLLECTION)
    task_collection = await get_collection(TASK_COLLECTION)
    project_oid = parse_object_id(task.project_id, "project_id")
    if await project_collection.count_documents({"_id": project_oid}, limit=1) == 0:
        raise HTTPException(status_code=400, detail="Proyecto no encontrado para la tarea")
    doc = jsonable_encoder(task)
    doc["project_id"] = project_oid
    now = datetime.now(timezone.utc)
    doc["created_at"] = now
    doc["updated_at"] = now
    result = await task_collection.insert_one(doc)
    created = await task_collection.find_one({"_id": result.inserted_id})
    if created is None:
        raise HTTPException(status_code=500, detail="No se pudo crear la tarea")
    return JSONResponse(status_code=201, content=jsonable_encoder(serialize_doc(created)))


@app.get("/api/v1/tasks/{task_id}", response_model=TaskInDB)
async def get_task(task_id: str):
    collection = await get_collection(TASK_COLLECTION)
    doc = await collection.find_one({"_id": parse_object_id(task_id, "task")})
    if doc is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return serialize_doc(doc)


@app.put("/api/v1/tasks/{task_id}", response_model=TaskInDB)
async def update_task(task_id: str, task: TaskUpdate):
    collection = await get_collection(TASK_COLLECTION)
    update_data = task.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se proporcionaron campos para actualizar")
    if "project_id" in update_data:
        update_data["project_id"] = parse_object_id(update_data["project_id"], "project_id")
    update_data["updated_at"] = datetime.now(timezone.utc)
    result = await collection.update_one({"_id": parse_object_id(task_id, "task")}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    doc = await collection.find_one({"_id": parse_object_id(task_id, "task")})
    return serialize_doc(doc)


@app.delete("/api/v1/tasks/{task_id}")
async def delete_task(task_id: str):
    collection = await get_collection(TASK_COLLECTION)
    result = await collection.delete_one({"_id": parse_object_id(task_id, "task")})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"deleted": True, "id": task_id}
