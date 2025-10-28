# INICIO RÁPIDO - Django con Oracle

## ✅ Proyecto Configurado

Tu proyecto Django ya está configurado con:
- ✅ App `myapp` creada
- ✅ Modelos: Producto y Cliente
- ✅ Vistas para CRUD
- ✅ Templates HTML con estilos
- ✅ Panel de administración
- ✅ URLs configuradas

## 🚀 Pasos para Ejecutar

### 1. Instalar cx_Oracle

```bash
pip install cx_Oracle
```

### 2. Configurar Oracle

Edita `DjangoProject/settings.py` (líneas 77-86):

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.oracle",
        "NAME": "localhost:1521/XEPDB1",  # ← CAMBIA ESTO
        "USER": "system",                   # ← CAMBIA ESTO
        "PASSWORD": "tu_contraseña",        # ← CAMBIA ESTO
        "OPTIONS": {
            "threaded": True,
        },
    }
}
```

### 3. Probar Conexión (Opcional)

```bash
python test_oracle.py
```

### 4. Crear Tablas en Oracle

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear Superusuario (Opcional)

```bash
python manage.py createsuperuser
```

### 6. Iniciar Servidor

```bash
python manage.py runserver
```

### 7. Abrir en el Navegador

```
http://localhost:8000/
```

## 📁 URLs Disponibles

| URL | Descripción |
|-----|-------------|
| `/` | Página principal |
| `/productos/` | Lista de productos |
| `/productos/crear/` | Crear producto |
| `/clientes/` | Lista de clientes |
| `/clientes/crear/` | Crear cliente |
| `/admin/` | Panel de administración |

## 🐳 Si usas Oracle en Docker

```bash
docker run -d \
  --name oracle-xe \
  -p 1521:1521 \
  -e ORACLE_PASSWORD=mypassword \
  gvenzl/oracle-xe

# Espera 2-3 minutos para que inicie
# Luego usa:
# NAME: localhost:1521/XEPDB1
# USER: system
# PASSWORD: mypassword
```

## 🔧 Script de Inicio Automático

```bash
./inicio.sh
```

Este script te guiará por todo el proceso.

## ⚠️ Problemas Comunes

### "cx_Oracle.DatabaseError: DPI-1047"
→ Instala Oracle Instant Client (ver ORACLE_CONFIG.md)

### "ORA-12541: TNS:no listener"
→ Verifica que Oracle esté corriendo

### "ORA-01017: invalid username/password"
→ Verifica tus credenciales

### Tablas no se crean
→ Ejecuta: `python manage.py migrate --run-syncdb`

## 📚 Archivos de Ayuda

- `README.md` - Documentación completa
- `ORACLE_CONFIG.md` - Guía de configuración Oracle
- `test_oracle.py` - Script para probar conexión
- `inicio.sh` - Script de inicio automático
- `verificar.sh` - Verificar estructura del proyecto

## 💡 Consejos

1. **Sin Oracle instalado?** Puedes cambiar temporalmente a SQLite para probar:
   ```python
   DATABASES = {
       "default": {
           "ENGINE": "django.db.backends.sqlite3",
           "NAME": BASE_DIR / "db.sqlite3",
       }
   }
   ```

2. **Ver logs de Oracle:**
   ```bash
   tail -f $ORACLE_HOME/diag/rdbms/*/trace/alert*.log
   ```

3. **Reiniciar Oracle:**
   ```bash
   # En SQL*Plus como sysdba:
   SHUTDOWN IMMEDIATE;
   STARTUP;
   ```

## 🎯 Siguiente Paso

```bash
# Opción 1: Usar el script automático
./inicio.sh

# Opción 2: Paso a paso
pip install cx_Oracle
python test_oracle.py  # Probar conexión
python manage.py migrate
python manage.py runserver
```

¡Listo! 🎉
# Configuración de ejemplo para Oracle
# Copia este archivo y edita los valores según tu configuración

[oracle]
# Ejemplo 1: Oracle Express Edition (XE)
host = localhost
port = 1521
service_name = XEPDB1
user = system
password = tu_contraseña

# Ejemplo 2: Oracle Standard/Enterprise
# host = localhost
# port = 1521
# service_name = ORCL
# user = tu_usuario
# password = tu_contraseña

# Ejemplo 3: Oracle Cloud
# host = tu_host_cloud.oraclecloud.com
# port = 1522
# service_name = tu_servicio_high
# user = ADMIN
# password = tu_contraseña

