# Proyecto Django con Oracle

Este es un proyecto Django configurado para conectarse a una base de datos Oracle con templates HTML para testear.

## 📋 Estructura del Proyecto

```
DjangoProject/
├── manage.py
├── requirements.txt
├── DjangoProject/
│   ├── __init__.py
│   ├── settings.py      # Configuración de Oracle
│   ├── urls.py          # URLs del proyecto
│   ├── wsgi.py
│   └── asgi.py
├── myapp/
│   ├── __init__.py
│   ├── models.py        # Modelos: Producto y Cliente
│   ├── views.py         # Vistas de la aplicación
│   ├── admin.py         # Configuración del admin
│   └── migrations/
└── templates/
    ├── base.html        # Template base
    ├── index.html       # Página principal
    ├── productos.html   # Lista de productos
    ├── clientes.html    # Lista de clientes
    ├── crear_producto.html
    └── crear_cliente.html
```

## 🚀 Instalación

### 1. Instalar Oracle Instant Client

Descarga e instala Oracle Instant Client desde:
https://www.oracle.com/database/technologies/instant-client/downloads.html

### 2. Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

### 3. Configurar la conexión a Oracle

Edita el archivo `DjangoProject/settings.py` y actualiza la configuración de DATABASES:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.oracle",
        "NAME": "localhost:1521/ORCL",  # Cambia por tu configuración
        "USER": "tu_usuario",            # Tu usuario de Oracle
        "PASSWORD": "tu_contraseña",     # Tu contraseña
        "OPTIONS": {
            "threaded": True,
        },
    }
}
```

### 4. Crear las migraciones y aplicarlas

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear un superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

## 🌐 URLs Disponibles

- `http://localhost:8000/` - Página principal
- `http://localhost:8000/productos/` - Lista de productos
- `http://localhost:8000/clientes/` - Lista de clientes
- `http://localhost:8000/productos/crear/` - Crear nuevo producto
- `http://localhost:8000/clientes/crear/` - Crear nuevo cliente
- `http://localhost:8000/admin/` - Panel de administración

## 📦 Modelos

### Producto
- nombre (CharField)
- precio (DecimalField)
- descripcion (TextField)
- fecha_creacion (DateTimeField)

### Cliente
- nombre (CharField)
- email (EmailField)
- telefono (CharField)
- direccion (TextField)
- fecha_registro (DateTimeField)

## 🎨 Features

- ✅ Conexión configurada con Oracle
- ✅ Modelos de ejemplo (Productos y Clientes)
- ✅ Templates HTML con estilos CSS
- ✅ CRUD básico para productos y clientes
- ✅ Panel de administración configurado
- ✅ Navegación intuitiva
- ✅ Diseño responsive

## 📝 Notas

- Asegúrate de tener Oracle Instant Client instalado y configurado correctamente
- Las tablas se crearán automáticamente en Oracle al ejecutar las migraciones
- Los templates incluyen estilos CSS inline para facilitar el testing

## 🔧 Solución de Problemas

### Error: "DPI-1047: Cannot locate a 64-bit Oracle Client library"
- Instala Oracle Instant Client y configura las variables de entorno correctamente

### Error de conexión a Oracle
- Verifica que el servicio de Oracle esté corriendo
- Comprueba que las credenciales sean correctas
- Verifica el formato del NAME (host:port/service_name)

## 📚 Documentación

- [Django Documentation](https://docs.djangoproject.com/)
- [cx_Oracle Documentation](https://cx-oracle.readthedocs.io/)
- [Oracle Database](https://www.oracle.com/database/)

