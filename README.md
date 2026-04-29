# APIProyect

Proyecto inicial de API NoSQL para respaldar un entregable académico.

## Estructura

- `src/main.py`: aplicación FastAPI
- `src/db.py`: conexión MongoDB con Motor
- `src/models.py`: modelos Pydantic
- `tests/test_main.py`: pruebas de integración

## Requisitos

Aún no se ha implementado el flujo exacto del proyecto porque no tengo el contenido completo del documento Word adjunto. Si me pasas los detalles del modelo de datos y los endpoints requeridos, ajusto la API al alcance del proyecto.

## Uso

1. Copia `.env.example` a `.env`.
2. Define `MONGODB_URI` y `MONGODB_DB`.
3. Ejecuta:

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Estructura de ejemplo

- CRUD genérico para un recurso `item` en MongoDB.
- Conexión por `MONGODB_URI`.

## Próximos pasos

- Validar los requerimientos del documento Word.
- Ajustar modelos de datos NoSQL según la base de datos no estructurada.
- Añadir endpoints específicos del proyecto.

## Planificación del desarrollo

Consulta el documento de planificación completo en `API_PLAN.md` para ver el diseño de datos, los endpoints propuestos, las validaciones, la arquitectura y el plan de trabajo.
