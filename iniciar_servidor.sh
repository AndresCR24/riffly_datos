#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          INICIANDO RIFFLY MUSIC PLATFORM                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

cd /Users/andresdavidcardenasramirez/Desktop/DjangoProject

# Verificar que Python y cx_Oracle estén disponibles
echo "1️⃣ Verificando dependencias..."
python -c "import cx_Oracle; print('   ✅ cx_Oracle instalado')" 2>&1 || { echo "   ❌ cx_Oracle no instalado"; exit 1; }
python -c "import django; print('   ✅ Django instalado')" 2>&1 || { echo "   ❌ Django no instalado"; exit 1; }

# Probar conexión
echo ""
echo "2️⃣ Probando conexión a Oracle..."
python -c "
import cx_Oracle
try:
    conn = cx_Oracle.connect('riffly_m', 'root123', 'localhost:1521/XE')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM USERS')
    count = cursor.fetchone()[0]
    print(f'   ✅ Conexión OK - {count} usuarios en BD')
    cursor.close()
    conn.close()
except Exception as e:
    print(f'   ❌ Error: {e}')
    exit(1)
" || exit 1

echo ""
echo "3️⃣ Verificando configuración de Django..."
python manage.py check --deploy 2>&1 | head -20

echo ""
echo "4️⃣ Listando archivos de templates..."
ls -la templates/ 2>&1 | head -20
ls -la templates/usuarios/ 2>&1 | head -10
ls -la templates/canciones/ 2>&1 | head -10

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                  INICIANDO SERVIDOR...                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Abre tu navegador en: http://localhost:8000/"
echo "📋 URLs disponibles:"
echo "   • http://localhost:8000/usuarios/"
echo "   • http://localhost:8000/canciones/"
echo "   • http://localhost:8000/generos/"
echo "   • http://localhost:8000/playlists/"
echo "   • http://localhost:8000/estadisticas/"
echo ""
echo "⏹️  Presiona Ctrl+C para detener el servidor"
echo ""

python manage.py runserver

