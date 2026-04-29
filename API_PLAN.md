# Planificación del desarrollo de la API de gestión de proyectos

## 1. Objetivo del proyecto
Diseñar e implementar una API RESTful para la gestión de proyectos informáticos y sus tareas, basada en MongoDB como sistema de persistencia NoSQL.

## 2. Alcance
Incluye:
- CRUD de proyectos
- CRUD de tareas
- Consultas por estado, nombre y tareas asociadas a proyectos
- Validación de datos y respuestas HTTP estandarizadas
- Manejo centralizado de errores
- Documentación OpenAPI/Swagger
- Pruebas unitarias e integración

No incluye en esta fase:
- Frontend
- Notificaciones
- Autenticación/usuarios (se deja como evolución futura)

## 3. Stakeholders
- Jefes de proyecto
- Desarrolladores
- Clientes finales

## 4. Requerimientos funcionales
1. CRUD de proyectos:
   - Crear proyecto
   - Listar proyectos
   - Obtener proyecto por id
   - Actualizar proyecto
   - Eliminar proyecto
2. CRUD de tareas:
   - Crear tarea asociada a proyecto
   - Listar tareas
   - Obtener tarea por id
   - Actualizar tarea
   - Eliminar tarea
3. Consultas avanzadas:
   - Filtrar tareas por estado
   - Buscar proyectos por nombre
   - Listar tareas de un proyecto
   - Buscar tareas por nombre

## 5. Requerimientos no funcionales
- Persistencia en MongoDB
- Validaciones de campos
- Manejo centralizado de errores
- Respuestas en JSON
- Documentación Swagger
- Arquitectura modular y escalable
- Cobertura de pruebas objetivo ≥ 80%
- Preparación para despliegue en cloud (Render / MongoDB Atlas)

## 6. Modelo de datos propuesto

### Colección `projects`
- `_id`: ObjectId
- `name`: string, obligatorio
- `description`: string, opcional
- `status`: string, opcional (ej. active, completed, paused)
- `start_date`: date, opcional
- `end_date`: date, opcional
- `metadata`: object, opcional
- `created_at`: datetime
- `updated_at`: datetime

### Colección `tasks`
- `_id`: ObjectId
- `project_id`: ObjectId, obligatorio
- `title`: string, obligatorio
- `description`: string, opcional
- `status`: string, obligatorio (ej. todo, in_progress, done)
- `priority`: string, opcional (low, medium, high)
- `due_date`: date, opcional
- `assigned_to`: string, opcional
- `created_at`: datetime
- `updated_at`: datetime

### Relación
- `project` 1:N `tasks`
- Las tareas referencian al proyecto mediante `project_id`

## 7. Endpoints API propuestos

Base: `/api/v1`

### Proyectos
- `GET /api/v1/projects`
- `POST /api/v1/projects`
- `GET /api/v1/projects/{project_id}`
- `PUT /api/v1/projects/{project_id}`
- `DELETE /api/v1/projects/{project_id}`
- `GET /api/v1/projects/{project_id}/tasks`

### Tareas
- `GET /api/v1/tasks`
- `POST /api/v1/tasks`
- `GET /api/v1/tasks/{task_id}`
- `PUT /api/v1/tasks/{task_id}`
- `DELETE /api/v1/tasks/{task_id}`

### Filtros opcionales
- `GET /api/v1/tasks?status=todo&project_id=...`
- `GET /api/v1/projects?name=...`

## 8. Validaciones clave
- `name` y `title` obligatorios
- `project_id` válido y existente al crear tarea
- `status` limitado a valores permitidos
- `ObjectId` válido para ids
- Fechas con formato ISO

## 9. Arquitectura y estructura recomendada

### Capas
- `src/main.py`: app FastAPI y routers
- `src/db.py`: conexión MongoDB y utilidades de acceso
- `src/models.py`: Pydantic models
- `src/schemas.py`: esquemas de entrada/salida (opcional)
- `src/services/`: lógica de negocio y acceso a datos
- `src/routers/`: rutas por dominio (`projects.py`, `tasks.py`)
- `src/core/`: configuración, constantes y manejo de errores
- `tests/`: pruebas unitarias e integración

### Tecnologías
- Python 3.12+ (implícito)
- FastAPI
- Motor (async MongoDB)
- Pydantic
- Uvicorn
- pytest + httpx
- python-dotenv

## 10. Plan de trabajo y entregables

### Fase 1: Diseño
- Definir modelo de datos
- Definir endpoints y rutas
- Preparar documentación del plan

### Fase 2: Implementación del backend
- Configurar FastAPI y MongoDB
- Implementar CRUD de proyectos
- Implementar CRUD de tareas
- Añadir filtros y consultas específicas

### Fase 3: Calidad
- Añadir validaciones y manejo de errores
- Agregar documentación OpenAPI
- Escribir pruebas unitarias e integración

### Fase 4: Despliegue y entrega
- Ajustar variables de entorno
- Preparar instrucciones de ejecución
- Opcional: crear Dockerfile para despliegue futuro

## 11. Cronograma sugerido

1. Día 1: análisis y diseño del modelo de datos
2. Día 2: CRUD de proyectos
3. Día 3: CRUD de tareas + relaciones
4. Día 4: filtros, validaciones y manejo de errores
5. Día 5: pruebas e integración
6. Día 6: documentación y ajuste final

## 12. Tareas específicas para el backlog

- [ ] Crear `Project` y `Task` models en `src/models.py`
- [ ] Separar routers en `src/routers/projects.py` y `src/routers/tasks.py`
- [ ] Implementar `src/services/project_service.py` y `src/services/task_service.py`
- [ ] Añadir middleware de errores y validación de ObjectId
- [ ] Documentar la API con Swagger
- [ ] Escribir tests para cada endpoint y caso de error
- [ ] Configurar despliegue en Render / MongoDB Atlas

## 13. Comentarios adicionales
- El documento original ya propone el enfoque MVP adecuado y la restricción obligatoria de MongoDB.
- En esta etapa, es recomendable mantener la API simple y clara, evitando funcionalidades adicionales como usuarios o notificaciones.
- El diseño referenciado entre proyectos y tareas es el más apropiado para un sistema académico y escalable.
