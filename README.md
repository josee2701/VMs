# VMS 🚀

Repositorio de una API REST construida con **FastAPI**, que gestiona autenticación con JWT, permisos basados en roles y funcionalidades de WebSocket para notificaciones en tiempo real.

## 📋 Descripción

Este proyecto implementa un servicio backend para gestionar usuarios, roles y comunicaciones vía WebSocket. Incluye:

- Autenticación con JWT.
- Gestión de permisos por rol (enum `Role`).
- CRUD de usuarios con asignación de roles.
- WebSocket de broadcast para notificaciones.
- Módulo de seguridad y hashing de contraseñas.

## 📂 Estructura del proyecto

```plaintext
VMS/
├── configs/           # Configuración de base de datos y constantes de seguridad
│   ├── db.py          # Inicialización de SQLAlchemy (SQLite por defecto)
│   └── security.py    # Variables y políticas JWT
├── models/            # Definición de modelos SQLModel y Pydantic
│   ├── role.py
│   ├── user.py
│   └── vm.py          # Otros modelos (ej. Vehículo)
├── routers/           # Rutas FastAPI agrupadas por funcionalidad
│   ├── auth.py        # Login y emisión de token JWT
│   ├── user.py        # CRUD de usuarios y asignación de roles
│   └── vm.py          # Rutas de ejemplo para VMs (opcional)
├── utils/             # Funciones auxiliares y dependencias
│   ├── auth.py        # Hashing de contraseñas y verificación
│   ├── deps.py        # Dependencias de seguridad para rutas
│   ├── ws_broadcaster.py # Lógica de broadcast por WebSocket
│   └── ws_manager.py  # Gestión de conexiones WebSocket
├── .env               # Variables de entorno (no está en Git)
├── main.py            # Punto de entrada de la aplicación
├── db.sqlite3         # Base de datos SQLite (ejemplo)
├── README.md          # Documentación de este repositorio
└── requirements.txt   # Dependencias Python
```

## 🚀 Requisitos

- Python 3.9 o superior
- pip

## 🔧 Instalación

1. Clonar el repositorio:  
   ```bash
   git clone https://github.com/josee2701/VMs.git
   cd VMS
   ```

2. Crear un entorno virtual y activarlo:  
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .\.venv\Scripts\activate    # Windows
   ```

3. Instalar dependencias:  
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## ▶️ Ejecución

Ejecuta la aplicación en modo desarrollo con autoreload:  
```bash
fastapi dev main.py
fastapi dev
```

- API REST disponible en: `http://localhost:8000`  
- Documentación interactiva Swagger en: `http://localhost:8000/docs`  
- Documentación ReDoc en: `http://localhost:8000/redoc`

## 📡 Endpoints de la API

### Auth (login)
- **POST /login**  
  Solicita JSON con `email` y `password`.  
  Devuelve un token JWT: `{ "access_token": string, "token_type": "bearer" }`.

### Usuarios (/users)
- **GET /users/**  
  Lista todos los usuarios.  
- **GET /users/{user_id}**  
  Obtiene un usuario por su ID.  
- **POST /users/**  
  Crea un usuario. Body JSON con `{ name, email, password, rol }`.  
- **PUT /users/{user_id}**  
  Actualiza campos de un usuario existente (parcialmente).  
- **DELETE /users/{user_id}**  
  Elimina un usuario.  

### VMs (/vms)
> Todas las rutas bajo `/vms` requieren token válido y algunas requieren rol administrador.  
- **GET /vms/**  
  Lista todas las VMs.  
- **GET /vms/{vm_id}**  
  Obtiene detalles de una VM.  
- **POST /vms/**  
  Crea una VM. Requiere rol administrador.  
- **PUT /vms/{vm_id}**  
  Actualiza una VM. Requiere rol administrador.  
- **DELETE /vms/{vm_id}**  
  Elimina una VM. Requiere rol administrador.

## 🛠️ Uso de WebSocket

Para suscribirte al canal de broadcast:  
```js
const ws = new WebSocket("ws://localhost:8000/ws/users");
ws.onmessage = (event) => console.log(event.data);
```

## 📈 Desarrollo y pruebas

Este proyecto es modular: añade rutas en `routers/`, define modelos en `models/` y protege tus endpoints con las dependencias de `utils/deps.py`. Luego, ejecuta el servidor y prueba las APIs con herramientas como Postman o HTTPie.


