# VMs

.
├── main.py              # crea app, incluye routers y tablas
├── configs
│   ├── db.py            # configuración de base de datos
│   └── security.py      # constantes y políticas de JWT
├── models
│   ├── role.py          # definición de Enum de roles
│   └── model.py         # modelos SQLModel + Pydantic
├── utils
│   ├── auth.py          # funciones de hashing y JWT
│   └── deps.py          # dependencias de FastAPI para seguridad
└── routers
    ├── auth.py          # login / emisión de token
    └── user.py          # CRUD de usuarios con permisos
