# CONFIGURACIÓN SIN ORM - ORACLE DIRECTO

## ✅ Proyecto Reconfigurado

El proyecto ahora está configurado para conectarse **directamente a Oracle sin usar ORM**.

### 🔧 Configuración Detectada

- **Usuario Oracle:** riffly_m
- **Host:** localhost:1521
- **SID/Service:** XE
- **Versión:** Oracle 21c Express Edition

---

## 📋 PASOS PARA EJECUTAR

### 1. Configurar la Contraseña

Edita `db_connection.py` (línea 13):

```python
DB_CONFIG = {
    'user': 'riffly_m',
    'password': 'TU_CONTRASEÑA_AQUI',  # ← CAMBIA ESTO
    'dsn': 'localhost:1521/XE',
    'encoding': 'UTF-8'
}
```

### 2. Crear las Tablas en Oracle

Abre el archivo `crear_tablas.sql` en PyCharm y ejecútalo en la consola SQL:

**Opción A: Desde PyCharm**
- Abre `crear_tablas.sql`
- Selecciona todo (Cmd+A)
- Haz clic en el botón "Execute" o presiona Ctrl+Enter
- Asegúrate de estar conectado a la BD `riffly_m`

**Opción B: Desde SQL*Plus**
```bash
sqlplus riffly_m/tu_contraseña@localhost:1521/XE
@crear_tablas.sql
```

### 3. Instalar cx_Oracle (si no está instalado)

```bash
pip install cx_Oracle
```

### 4. Probar la Conexión

```bash
python db_connection.py
```

Deberías ver:
```
🔍 Probando conexión a Oracle...
   Usuario: riffly_m
   DSN: localhost:1521/XE
--------------------------------------------------
✅ Conexión exitosa!
📊 Versión de Oracle: Oracle Database 21c...
```

### 5. Iniciar Django (sin migraciones)

```bash
python manage.py runserver
```

### 6. Probar en el Navegador

```
http://localhost:8000/
```

---

## 📂 Archivos Modificados

### ✅ `db_connection.py` (NUEVO)
- Maneja la conexión directa a Oracle
- Funciones: `execute_query()`, `execute_dml()`, `call_procedure()`
- No usa ORM de Django

### ✅ `myapp/views.py` (MODIFICADO)
- Usa SQL directo en lugar de ORM
- Ejemplo:
  ```python
  query = "SELECT * FROM PRODUCTOS ORDER BY FECHA_CREACION DESC"
  productos = execute_query(query)
  ```

### ✅ `crear_tablas.sql` (NUEVO)
- Script SQL para crear:
  - Tabla PRODUCTOS
  - Tabla CLIENTES
  - Secuencias para IDs
  - Datos de prueba

### ✅ `templates/*.html` (MODIFICADOS)
- Adaptados para usar nombres de columnas de Oracle (mayúsculas)
- Ejemplo: `{{ producto.NOMBRE }}` en lugar de `{{ producto.nombre }}`

### ✅ `settings.py` (MODIFICADO)
- SQLite solo para el admin de Django
- Oracle se maneja directamente con cx_Oracle

---

## 🎯 Estructura de las Tablas

### PRODUCTOS
```sql
ID              NUMBER (auto-increment con secuencia)
NOMBRE          VARCHAR2(100)
PRECIO          NUMBER(10,2)
DESCRIPCION     CLOB
FECHA_CREACION  TIMESTAMP (default SYSDATE)
```

### CLIENTES
```sql
ID              NUMBER (auto-increment con secuencia)
NOMBRE          VARCHAR2(100)
EMAIL           VARCHAR2(100) UNIQUE
TELEFONO        VARCHAR2(20)
DIRECCION       VARCHAR2(500)
FECHA_REGISTRO  TIMESTAMP (default SYSDATE)
```

---

## 📝 Ejemplos de Uso

### Consultar Datos
```python
from db_connection import execute_query

# Obtener todos los productos
query = "SELECT * FROM PRODUCTOS"
productos = execute_query(query)

# Consulta con parámetros
query = "SELECT * FROM PRODUCTOS WHERE PRECIO > :precio"
productos = execute_query(query, {'precio': 100})
```

### Insertar Datos
```python
from db_connection import execute_dml

query = """
    INSERT INTO PRODUCTOS (NOMBRE, PRECIO, DESCRIPCION, FECHA_CREACION)
    VALUES (:nombre, :precio, :descripcion, SYSDATE)
"""
params = {
    'nombre': 'Producto Nuevo',
    'precio': 99.99,
    'descripcion': 'Descripción del producto'
}
execute_dml(query, params)
```

### Actualizar Datos
```python
query = "UPDATE PRODUCTOS SET PRECIO = :precio WHERE ID = :id"
execute_dml(query, {'precio': 120.50, 'id': 1})
```

### Eliminar Datos
```python
query = "DELETE FROM PRODUCTOS WHERE ID = :id"
execute_dml(query, {'id': 1})
```

---

## 🔍 Verificar que Todo Funciona

### 1. Verificar Tablas en Oracle
```sql
SELECT table_name FROM user_tables WHERE table_name IN ('PRODUCTOS', 'CLIENTES');
```

### 2. Verificar Datos
```sql
SELECT COUNT(*) FROM PRODUCTOS;
SELECT COUNT(*) FROM CLIENTES;
```

### 3. Probar la App
```bash
# Terminal 1
python db_connection.py

# Terminal 2
python manage.py runserver
```

---

## ⚠️ IMPORTANTE - SIN ORM

Este proyecto **NO USA ORM de Django**:

❌ **NO funciona:**
```python
Producto.objects.all()  # NO
Cliente.objects.create()  # NO
```

✅ **SÍ funciona:**
```python
execute_query("SELECT * FROM PRODUCTOS")  # SÍ
execute_dml("INSERT INTO PRODUCTOS ...", params)  # SÍ
```

---

## 🐛 Solución de Problemas

### Error: "ORA-00942: table or view does not exist"
→ Ejecuta `crear_tablas.sql` primero

### Error: "ORA-01017: invalid username/password"
→ Verifica la contraseña en `db_connection.py`

### Error: "No module named 'cx_Oracle'"
→ Ejecuta: `pip install cx_Oracle`

### Las tablas están vacías
→ El script `crear_tablas.sql` incluye datos de prueba

### Error: "DPI-1047: Cannot locate a 64-bit Oracle Client"
→ Instala Oracle Instant Client

---

## 📋 Checklist Final

- [ ] Configurar contraseña en `db_connection.py`
- [ ] Ejecutar `crear_tablas.sql` en PyCharm
- [ ] Instalar cx_Oracle: `pip install cx_Oracle`
- [ ] Probar conexión: `python db_connection.py`
- [ ] Iniciar servidor: `python manage.py runserver`
- [ ] Abrir navegador: `http://localhost:8000/`

---

## 🎉 ¡Listo!

El proyecto está configurado para usar **Oracle directamente sin ORM**.
Todas las operaciones de base de datos se hacen con SQL nativo.

