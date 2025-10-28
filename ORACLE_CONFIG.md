# Guía de Configuración de Oracle para Django

## 📝 Configuración de Oracle en macOS

### 1. Instalar Oracle Instant Client

```bash
# Descargar desde: https://www.oracle.com/database/technologies/instant-client/macos-intel-x86-downloads.html
# O con Homebrew:
brew tap InstantClientTap/instantclient
brew install instantclient-basic
brew install instantclient-sqlplus
```

### 2. Configurar variables de entorno

Agrega esto a tu `~/.zshrc`:

```bash
export ORACLE_HOME=/usr/local/lib
export LD_LIBRARY_PATH=$ORACLE_HOME
export PATH=$ORACLE_HOME:$PATH
```

Luego ejecuta:
```bash
source ~/.zshrc
```

### 3. Instalar cx_Oracle

```bash
pip install cx_Oracle
```

## 🔧 Configuraciones de Oracle en settings.py

### Opción 1: Conexión por TNS Name
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.oracle",
        "NAME": "ORCL",  # Tu TNS name
        "USER": "tu_usuario",
        "PASSWORD": "tu_contraseña",
    }
}
```

### Opción 2: Conexión por Host/Port
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.oracle",
        "NAME": "localhost:1521/XEPDB1",  # host:port/service_name
        "USER": "tu_usuario",
        "PASSWORD": "tu_contraseña",
        "OPTIONS": {
            "threaded": True,
        },
    }
}
```

### Opción 3: Usando Easy Connect String
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.oracle",
        "NAME": "//localhost:1521/XEPDB1",
        "USER": "tu_usuario",
        "PASSWORD": "tu_contraseña",
    }
}
```

## 🧪 Probar la conexión

Crea un archivo `test_oracle.py` en la raíz del proyecto:

```python
import cx_Oracle

try:
    # Cambia estos valores por tus credenciales
    connection = cx_Oracle.connect(
        user="tu_usuario",
        password="tu_contraseña",
        dsn="localhost:1521/XEPDB1"
    )
    
    print("✅ Conexión exitosa a Oracle!")
    print(f"Versión de Oracle: {connection.version}")
    connection.close()
    
except cx_Oracle.Error as error:
    print(f"❌ Error de conexión: {error}")
```

## 📊 Ejemplos de configuración comunes

### Oracle Express Edition (XE)
```python
"NAME": "localhost:1521/XEPDB1",
"USER": "system",
```

### Oracle Cloud
```python
"NAME": "your-db_high",  # Usando wallet
"USER": "ADMIN",
```

### Oracle en Docker
```bash
docker run -d -p 1521:1521 -e ORACLE_PASSWORD=mypassword gvenzl/oracle-xe
```

```python
"NAME": "localhost:1521/XEPDB1",
"USER": "system",
"PASSWORD": "mypassword",
```

## 🚨 Solución de problemas comunes

### Error: "DPI-1047: Cannot locate a 64-bit Oracle Client library"
- Instala Oracle Instant Client
- Verifica las variables de entorno ORACLE_HOME y LD_LIBRARY_PATH

### Error: "ORA-12541: TNS:no listener"
- Verifica que el listener de Oracle esté corriendo
- Ejecuta: `lsnrctl status`

### Error: "ORA-01017: invalid username/password"
- Verifica tus credenciales
- Intenta conectarte con SQL*Plus primero

### Error: "ORA-12514: TNS:listener does not currently know of service"
- Verifica el service_name
- Ejecuta: `lsnrctl services` para ver servicios disponibles

## 📝 Comandos útiles

```bash
# Ver servicios de Oracle
lsnrctl services

# Conectar con SQL*Plus
sqlplus usuario/contraseña@localhost:1521/XEPDB1

# Ver tablas creadas por Django
SELECT table_name FROM user_tables WHERE table_name LIKE 'PRODUCTOS' OR table_name LIKE 'CLIENTES';
```

