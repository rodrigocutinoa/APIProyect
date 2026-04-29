from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    name: str = Field(..., title="Nombre del proyecto")
    description: Optional[str] = Field(None, title="Descripción del proyecto")
    status: Optional[str] = Field("active", title="Estado del proyecto")
    metadata: Optional[dict] = Field(default_factory=dict, title="Metadatos adicionales")


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, title="Nombre del proyecto")
    description: Optional[str] = Field(None, title="Descripción del proyecto")
    status: Optional[str] = Field(None, title="Estado del proyecto")
    metadata: Optional[dict] = Field(None, title="Metadatos adicionales")


class ProjectInDB(ProjectBase):
    id: str = Field(..., alias="_id")
    created_at: Optional[datetime] = Field(None, title="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, title="Fecha de última actualización")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "_id": "644c6d4f70f7f7c7f7c7f7c7",
                "name": "Proyecto de ejemplo",
                "description": "Descripción del proyecto",
                "status": "active",
                "metadata": {"cliente": "ACME"},
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-01T00:00:00Z"
            }
        }
    }


class TaskBase(BaseModel):
    title: str = Field(..., title="Título de la tarea")
    description: Optional[str] = Field(None, title="Descripción de la tarea")
    status: Optional[str] = Field("todo", title="Estado de la tarea")
    priority: Optional[str] = Field(None, title="Prioridad de la tarea")
    due_date: Optional[str] = Field(None, title="Fecha límite")
    assigned_to: Optional[str] = Field(None, title="Persona asignada")
    metadata: Optional[dict] = Field(default_factory=dict, title="Metadatos adicionales")


class TaskCreate(TaskBase):
    project_id: str = Field(..., title="ID del proyecto")


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, title="Título de la tarea")
    description: Optional[str] = Field(None, title="Descripción de la tarea")
    status: Optional[str] = Field(None, title="Estado de la tarea")
    priority: Optional[str] = Field(None, title="Prioridad de la tarea")
    due_date: Optional[str] = Field(None, title="Fecha límite")
    assigned_to: Optional[str] = Field(None, title="Persona asignada")
    metadata: Optional[dict] = Field(None, title="Metadatos adicionales")
    project_id: Optional[str] = Field(None, title="ID del proyecto")


class TaskInDB(TaskBase):
    id: str = Field(..., alias="_id")
    project_id: str = Field(..., title="ID del proyecto")
    created_at: Optional[datetime] = Field(None, title="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, title="Fecha de última actualización")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "_id": "644c6d4f70f7f7c7f7c7f7c7",
                "project_id": "644c6d4f70f7f7c7f7c7f7c6",
                "title": "Tarea de ejemplo",
                "status": "todo",
                "priority": "high",
                "metadata": {"tipo": "bug"},
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-01T00:00:00Z"
            }
        }
    }
