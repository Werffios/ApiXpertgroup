# API de Chatbot con FastAPI y OpenAI

Este proyecto es una API RESTful desarrollada con FastAPI que se integra con la API de OpenAI para ofrecer un servicio de chatbot. La API permite configurar roles para el chatbot, persistir las conversaciones en una base de datos SQLite y consultar el historial de interacciones por usuario.

## Objetivo General

Crear una API RESTful utilizando FastAPI que consuma la API de OpenAI para simular un chatbot configurable con roles. La aplicación debe implementar persistencia de datos usando SQLite, seguir buenas prácticas de desarrollo, y proporcionar endpoints funcionales y bien documentados.

## Características

- **Integración con OpenAI**: Permite configurar un rol específico (por ejemplo, "experto en evaluación de riesgos laborales") para que el chatbot responda con un enfoque y terminología adecuados.
- **Endpoints documentados**: La API cuenta con endpoints claros para gestionar usuarios, enviar preguntas y consultar el historial.
- **Persistencia de datos**: Utiliza SQLite para almacenar usuarios, roles y el historial de conversaciones.
- **Arquitectura modular**: El código está organizado en módulos para separar la lógica de negocio, el acceso a datos y la definición de la API.
- **Manejo de errores**: La API gestiona excepciones comunes, como usuarios no encontrados o problemas de conexión.
- **Pruebas unitarias**: Incluye pruebas para los endpoints principales, utilizando mocks para simular las respuestas de la API de OpenAI.
- **Configuración por entorno**: Utiliza variables de entorno para gestionar configuraciones sensibles como la clave de la API de OpenAI.

## Estructura del Proyecto

El proyecto sigue una estructura modular para facilitar el mantenimiento y la escalabilidad:

```
/
|-- app/
|   |-- api/
|   |   `-- routes.py         # Endpoints de la API
|   |-- core/
|   |   `-- config.py         # Configuración de la aplicación (variables de entorno)
|   |-- db/
|   |   |-- crud.py           # Operaciones CRUD para la base de datos
|   |   |-- database.py       # Configuración de la conexión a la base de datos
|   |   `-- models.py         # Modelos de datos de SQLAlchemy
|   |-- schemas/
|   |   `-- schemas.py        # Esquemas de Pydantic para validación de datos
|   `-- services/
|       `-- openai_service.py # Lógica para interactuar con la API de OpenAI
|-- tests/
|   `-- test_api.py           # Pruebas unitarias para la API
|-- main.py                   # Punto de entrada de la aplicación
|-- requirements.txt          # Dependencias del proyecto
`-- .env                      # Archivo para variables de entorno (no incluido en el repo)
```

## Endpoints de la API

La API expone los siguientes endpoints:

### 1. Inicializar Usuario

- **Endpoint**: `POST /init_user`
- **Descripción**: Crea un nuevo usuario con un rol específico.
- **Request Body**:
  ```json
  {
    "username": "nombre_de_usuario",
    "role": "rol_del_usuario"
  }
  ```
- **Respuesta Exitosa (200)**:
  ```json
  {
    "username": "nombre_de_usuario",
    "role": "rol_del_usuario",
    "id": 1
  }
  ```

### 2. Enviar Mensaje al Chatbot

- **Endpoint**: `POST /ask`
- **Descripción**: Envía un mensaje al chatbot en nombre de un usuario y guarda la interacción.
- **Query Params**: `username={nombre_de_usuario}`
- **Request Body**:
  ```json
  {
    "message": "Tu pregunta aquí"
  }
  ```
- **Respuesta Exitosa (200)**:
  ```json
  {
    "response": "Respuesta generada por el chatbot."
  }
  ```

### 3. Consultar Historial

- **Endpoint**: `GET /history/{username}`
- **Descripción**: Obtiene el historial de conversaciones de un usuario.
- **Respuesta Exitosa (200)**:
  ```json
  {
    "history": [
      {
        "id": 1,
        "user_id": 1,
        "message": "Tu pregunta aquí",
        "response": "Respuesta generada por el chatbot."
      }
    ]
  }
  ```

### 4. Verificar Estado del Servicio

- **Endpoint**: `GET /health`
- **Descripción**: Comprueba el estado del servicio y la conexión a la base de datos.
- **Respuesta Exitosa (200)**:
  ```json
  {
    "service_status": "OK",
    "database_status": "Todo bien, todo ok!"
  }
  ```

## Cómo Replicar el Proyecto en Local

Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local.

### Prerrequisitos

- Python 3.8 o superior.
- `pip` para la gestión de paquetes.

### 1. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_DIRECTORIO>
```

### 2. Crear un Entorno Virtual

Es una buena práctica trabajar en un entorno virtual para aislar las dependencias del proyecto.

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

Instala todas las dependencias necesarias que se encuentran en el archivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crea un archivo llamado `.env` en la raíz del proyecto y añade tu clave de la API de OpenAI.

```
OPENAI_API_KEY="tu_api_key_de_openai"
```

### 5. Ejecutar la Aplicación

Usa `uvicorn` para iniciar el servidor de la API.

```bash
uvicorn main:app --reload
```

La opción `--reload` reiniciará el servidor automáticamente cada vez que detecte un cambio en el código.

La API estará disponible en `http://127.0.0.1:8000`.

### 6. Acceder a la Documentación Interactiva

FastAPI genera automáticamente una documentación interactiva de la API. Puedes acceder a ella en las siguientes URLs:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### 7. Ejecutar las Pruebas

Para asegurarte de que todo funciona correctamente, puedes ejecutar las pruebas unitarias con `pytest`.

```bash
pytest
```

## Tecnologías Utilizadas

- **FastAPI**: Framework web para construir APIs con Python.
- **SQLAlchemy**: ORM para interactuar con la base de datos.
- **SQLite**: Motor de base de datos ligero y sin servidor.
- **Pydantic**: Biblioteca para validación de datos.
- **OpenAI API**: Servicio de IA para generar respuestas de chatbot.
- **Pytest**: Framework para escribir y ejecutar pruebas.
- **Uvicorn**: Servidor ASGI para ejecutar aplicaciones FastAPI.

