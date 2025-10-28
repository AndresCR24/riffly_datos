#!/bin/bash

# Script para verificar la instalación y configuración del proyecto

echo "🔍 Verificando estructura del proyecto..."
echo ""

# Verificar archivos principales
files=(
    "manage.py"
    "requirements.txt"
    "README.md"
    "DjangoProject/settings.py"
    "DjangoProject/urls.py"
    "myapp/models.py"
    "myapp/views.py"
    "myapp/admin.py"
    "templates/base.html"
    "templates/index.html"
    "templates/productos.html"
    "templates/clientes.html"
    "templates/crear_producto.html"
    "templates/crear_cliente.html"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file - NO ENCONTRADO"
    fi
done

echo ""
echo "📦 Instalación completada!"
echo ""
echo "🚀 Próximos pasos:"
echo "1. Instalar cx_Oracle: pip install cx_Oracle"
echo "2. Configurar Oracle en DjangoProject/settings.py"
echo "3. Ejecutar: python manage.py makemigrations"
echo "4. Ejecutar: python manage.py migrate"
echo "5. Ejecutar: python manage.py runserver"
echo ""
echo "🌐 Acceder a: http://localhost:8000/"

