#!/bin/bash

# Script de configuración para proyecto Django + Oracle SIN ORM
# Usuario: riffly_m
# Base de datos: localhost:1521/XE

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   CONFIGURACIÓN DJANGO + ORACLE (SIN ORM)                 ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Verificar cx_Oracle
echo "📦 Verificando cx_Oracle..."
python -c "import cx_Oracle" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ cx_Oracle está instalado${NC}"
else
    echo -e "${YELLOW}⚠️  cx_Oracle no está instalado${NC}"
    read -p "¿Deseas instalarlo ahora? (s/n): " install
    if [ "$install" = "s" ] || [ "$install" = "S" ]; then
        pip install cx_Oracle
    fi
fi

echo ""

# 2. Configurar contraseña
echo "🔐 Configuración de la base de datos"
echo "   Usuario: riffly_m"
echo "   DSN: localhost:1521/XE"
echo ""
read -sp "Ingresa la contraseña para riffly_m: " password
echo ""

# Actualizar db_connection.py con la contraseña
sed -i.bak "s/'password': 'tu_contraseña'/'password': '$password'/" db_connection.py
echo -e "${GREEN}✅ Contraseña configurada en db_connection.py${NC}"

echo ""

# 3. Probar conexión
echo "🧪 Probando conexión a Oracle..."
python db_connection.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Conexión exitosa${NC}"
else
    echo -e "${RED}❌ Error de conexión${NC}"
    echo "   Verifica que Oracle esté corriendo y las credenciales sean correctas"
    exit 1
fi

echo ""

# 4. Verificar si las tablas existen
echo "📊 Verificando tablas en Oracle..."
python -c "
from db_connection import execute_query
result = execute_query('SELECT table_name FROM user_tables WHERE table_name IN (\'PRODUCTOS\', \'CLIENTES\')')
if result and len(result) >= 2:
    print('✅ Tablas PRODUCTOS y CLIENTES existen')
    exit(0)
else:
    print('⚠️  Las tablas no existen o están incompletas')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${YELLOW}📝 Necesitas crear las tablas en Oracle${NC}"
    echo ""
    echo "Opciones:"
    echo "1. Abrir crear_tablas.sql en PyCharm y ejecutarlo"
    echo "2. Ejecutar desde SQL*Plus:"
    echo "   sqlplus riffly_m/$password@localhost:1521/XE @crear_tablas.sql"
    echo ""
    read -p "¿Ya creaste las tablas? (s/n): " created
    if [ "$created" != "s" ] && [ "$created" != "S" ]; then
        echo ""
        echo "Por favor, crea las tablas primero y vuelve a ejecutar este script."
        exit 1
    fi
fi

echo ""

# 5. Iniciar servidor
echo "🚀 Todo listo!"
echo ""
echo "Para iniciar el servidor ejecuta:"
echo -e "${GREEN}python manage.py runserver${NC}"
echo ""
echo "Luego abre en tu navegador:"
echo -e "${GREEN}http://localhost:8000/${NC}"
echo ""

read -p "¿Deseas iniciar el servidor ahora? (s/n): " start
if [ "$start" = "s" ] || [ "$start" = "S" ]; then
    python manage.py runserver
fi

