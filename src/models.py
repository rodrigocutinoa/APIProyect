from pydantic import BaseModel, Field
from typing import Optional

class ItemBase(BaseModel):
    name: str = Field(..., title="Nombre del ítem")
    description: Optional[str] = Field(None, title="Descripción del ítem")
    metadata: Optional[dict] = Field(default_factory=dict, title="Metadatos adicionales")

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, title="Nombre del ítem")
    description: Optional[str] = Field(None, title="Descripción del ítem")
    metadata: Optional[dict] = Field(None, title="Metadatos adicionales")

class ItemInDB(ItemBase):
    id: str = Field(..., alias="_id")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Documento de ejemplo",
                "description": "Ejemplo de descripción",
                "metadata": {"categoria": "demo"}
            }
        }
