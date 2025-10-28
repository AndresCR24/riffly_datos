#!/bin/bash

# Script de inicio rápido para el proyecto Django + Oracle

echo "🚀 Iniciando proyecto Django con Oracle"
echo "========================================"
echo ""

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar Python
if command_exists python; then
    echo "✅ Python encontrado: $(python --version)"
else
    echo "❌ Python no encontrado"
    exit 1
fi

# Verificar pip
if command_exists pip; then
    echo "✅ pip encontrado"
else
    echo "❌ pip no encontrado"
    exit 1
fi

echo ""
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

echo ""
echo "⚙️ IMPORTANTE: Configura Oracle en DjangoProject/settings.py"
echo ""
echo "Edita las siguientes líneas:"
echo '  "NAME": "localhost:1521/XEPDB1",  # Tu configuración'
echo '  "USER": "tu_usuario",              # Tu usuario'
echo '  "PASSWORD": "tu_contraseña",       # Tu contraseña'
echo ""

read -p "¿Has configurado Oracle? (s/n): " configured

if [ "$configured" = "s" ] || [ "$configured" = "S" ]; then
    echo ""
    echo "🧪 Probando conexión a Oracle..."
    python test_oracle.py

    echo ""
    read -p "¿La conexión fue exitosa? (s/n): " connection_ok

    if [ "$connection_ok" = "s" ] || [ "$connection_ok" = "S" ]; then
        echo ""
        echo "📊 Creando migraciones..."
        python manage.py makemigrations

        echo ""
        echo "🔄 Aplicando migraciones..."
        python manage.py migrate

        echo ""
        echo "👤 ¿Deseas crear un superusuario? (s/n): "
        read create_super

        if [ "$create_super" = "s" ] || [ "$create_super" = "S" ]; then
            python manage.py createsuperuser
        fi

        echo ""
        echo "✅ ¡Todo listo!"
        echo ""
        echo "🌐 Iniciando servidor..."
        echo "   Accede a: http://localhost:8000/"
        echo ""
        python manage.py runserver
    else
        echo ""
        echo "⚠️ Configura la conexión a Oracle primero"
        echo "   Lee el archivo ORACLE_CONFIG.md para ayuda"
    fi
else
    echo ""
    echo "📝 Pasos siguientes:"
    echo "1. Edita DjangoProject/settings.py"
    echo "2. Configura las credenciales de Oracle"
    echo "3. Ejecuta nuevamente: ./inicio.sh"
fi

