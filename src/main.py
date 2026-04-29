from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from bson import ObjectId
from typing import List

from .db import get_collection
from .models import ItemCreate, ItemUpdate, ItemInDB

app = FastAPI(title="APIProyect", version="0.1.0")

COLLECTION_NAME = "items"


@app.on_event("startup")
async def startup_event():
    await get_collection(COLLECTION_NAME)


@app.post("/items", response_model=ItemInDB)
async def create_item(item: ItemCreate):
    collection = await get_collection(COLLECTION_NAME)
    doc = jsonable_encoder(item)
    result = await collection.insert_one(doc)
    created = await collection.find_one({"_id": result.inserted_id})
    if created is None:
        raise HTTPException(status_code=500, detail="No se pudo crear el ítem")
    created["_id"] = str(created["_id"])
    return JSONResponse(status_code=201, content=created)


@app.get("/items", response_model=List[ItemInDB])
async def list_items():
    collection = await get_collection(COLLECTION_NAME)
    cursor = collection.find()
    items = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        items.append(doc)
    return items


@app.get("/items/{item_id}", response_model=ItemInDB)
async def get_item(item_id: str):
    collection = await get_collection(COLLECTION_NAME)
    doc = await collection.find_one({"_id": ObjectId(item_id)})
    if doc is None:
        raise HTTPException(status_code=404, detail="Ítem no encontrado")
    doc["_id"] = str(doc["_id"])
    return doc


@app.put("/items/{item_id}", response_model=ItemInDB)
async def update_item(item_id: str, item: ItemUpdate):
    collection = await get_collection(COLLECTION_NAME)
    update_data = {k: v for k, v in item.dict(exclude_unset=True).items()}
    if not update_data:
        raise HTTPException(status_code=400, detail="No se proporcionaron campos para actualizar")
    result = await collection.update_one({"_id": ObjectId(item_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Ítem no encontrado")
    doc = await collection.find_one({"_id": ObjectId(item_id)})
    doc["_id"] = str(doc["_id"])
    return doc


@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    collection = await get_collection(COLLECTION_NAME)
    result = await collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Ítem no encontrado")
    return {"deleted": True, "id": item_id}
