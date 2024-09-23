# API de Lista de Tareas

## Requisitos

- Python 3.x
- pip (administrador de paquetes de Python)

## Descripción

Este es un servicio API RESTFUL con DRF simple que realiza las operaciones CRUD para una TODO list.
Además realiza las mismas operaciones usando Strawberry GraphQL

## Contacto

**Desarrollador:** Ing. Daniel Torres  
**GitHub:** [https://github.com/dfilth

## Versiones

- **Versión API:** 1.0

## Uso

La API está disponible en el siguiente endpoint base:

http://localhost:8000/tasks/

## Doc

http://localhost:8000/docs/#/tasks/

## Ejecución con Docker

Para ejecutar el proyecto mediante Docker, sigue estos pasos:

Ejecuta el siguiente comando para levantar los contenedores de la aplicación:

```bash
docker compose up -d
```

Comprueba que los contenedores estén activos:

```bash
docker ps
```

Luego, el proyecto estará listo para usar:
http://localhost:8000/tasks/

Adicionalmente se puede ingresar dentro del contendor y ejecutar comandos de django u otros como:

Crear superusuario:
- docker-compose exec web bash
- python manage.py createsuperuser

Aplicar y Actualizar migraciones:
- docker-compose exec web bash
- python manage.py makemigrations
- python manage.py migrate

## Disponemos de las siguientes urls:

GET /tasks/ - Obtener todas las tareas.
POST /tasks/ - Crear una nueva tarea.
GET /tasks/{id}/ - Obtener una tarea por su ID.
PUT /tasks/{id}/ - Actualizar una tarea por su ID.
DELETE /tasks/{id}/ - Eliminar una tarea por su ID.

## Información de envío de datos modelo Task

{
"id": 1,
"title": "Sample Task",
"description": "This is a sample task",
"completed": false
}

Opcionalmente, puedes ver en la consola el estado del servicio:

```bash
docker logs -f {nombre_del_contenedor} ejm: todolist-web-1
```

## Ejecución Local

Para ejecutar el proyecto de forma local, sigue estos pasos:

1. Crear y activar un entorno virtual:

- python -m venv venv
- source venv/bin/activate

2. Instalar dependencias:

- pip install -r requirements.txt

3. Realizar las migraciones:

- python manage.py migrate

4. Creación de superuser para acceder desde admin

- python manage.py createsuperuser

5. Ejecutar el servidor de desarrollo:

- python manage.py runserver
- o python -m uvicorn todo_list.asgi:application

6. Acceder a la aplicación:

- Abre tu navegador y visita http://localhost:8000 para ver la aplicación en funcionamiento.
- http://localhost:8000/tasks
- http://127.0.0.1:8000/admin
- http://127.0.0.1:8000/graphql

## Uso de graphql:

Una vez en la api de graphql podemos ir enviando los diferentes queries:
- http://127.0.0.1:8000/graphql

1. Crear tarea:
   mutation {
   createTask(title: "New Task", description: "Task Description", completed:true) {
   id
   title
   description
   completed
   }
   }
2. Obtener todas las tareas:
   {
   allTasks {
   id
   title
   description
   completed
   }
   }

3. Obtener tarea por id:
   {
   taskById(id: 2) {
   id
   title
   description
   completed
   }
   }

4. Actualizar tarea:
   mutation {
   updateTask(id: 2, title: "Updated Task", description: "Updated description", completed: true) {
   id
   title
   description
   completed
   }
   }

5. Eliminar tarea:
   mutation {
   deleteTask(id: 1)
   }

## Herramientas de formateo y corrección

Podemos usar flake8 para buscar posibles inconsistencias en los archivos en cuanto a formato:

- flake8 todo_list/tasks/

Usamos black para corregir las inconsistencias:

- black todolist (formatea de forma general)
- black todolist --line-length 79 (especificando una longitud específica siguiendo PEP8)

## Pruebas

Para ejecutar las pruebas:

```bash
pytest todolist/tests/tasks/
```