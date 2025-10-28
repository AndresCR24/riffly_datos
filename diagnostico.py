#!/usr/bin/env python
"""
Script de diagnóstico para verificar la conexión y las vistas
"""
import sys
import os

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')

print("="*70)
print("DIAGNÓSTICO DE CONEXIÓN - RIFFLY MUSIC PLATFORM")
print("="*70)

# Test 1: Verificar cx_Oracle
print("\n1. Verificando cx_Oracle...")
try:
    import cx_Oracle
    print(f"   ✅ cx_Oracle instalado (versión: {cx_Oracle.version})")
except ImportError as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: Conexión directa
print("\n2. Probando conexión directa a Oracle...")
try:
    conn = cx_Oracle.connect(
        user='riffly_m',
        password='root123',
        dsn='localhost:1521/XE'
    )
    print("   ✅ Conexión exitosa!")

    cursor = conn.cursor()

    # Verificar tablas
    print("\n3. Verificando tablas...")
    tablas = ['USERS', 'SONGS', 'GENRES', 'PLAYLISTS', 'COMMENTS']
    for tabla in tablas:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cursor.fetchone()[0]
            print(f"   ✅ {tabla}: {count} registros")
        except Exception as e:
            print(f"   ❌ {tabla}: {e}")

    # Obtener datos de ejemplo
    print("\n4. Obteniendo datos de ejemplo...")
    try:
        cursor.execute("SELECT USER_ID, USERNAME, EMAIL FROM USERS WHERE ROWNUM <= 3")
        users = cursor.fetchall()
        print(f"   Usuarios encontrados: {len(users)}")
        for user in users:
            print(f"      - ID: {user[0]}, Username: {user[1]}, Email: {user[2]}")
    except Exception as e:
        print(f"   ❌ Error obteniendo usuarios: {e}")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"   ❌ Error de conexión: {e}")
    print(f"   Tipo: {type(e).__name__}")
    sys.exit(1)

# Test 3: Probar funciones de db_connection
print("\n5. Probando funciones de db_connection.py...")
try:
    from db_connection import execute_query, execute_single

    total = execute_single("SELECT COUNT(*) FROM USERS")
    print(f"   ✅ execute_single: {total} usuarios")

    usuarios = execute_query("SELECT USER_ID, USERNAME FROM USERS WHERE ROWNUM <= 3")
    if usuarios:
        print(f"   ✅ execute_query: {len(usuarios)} usuarios obtenidos")
        for u in usuarios:
            print(f"      - {u}")
    else:
        print(f"   ⚠️ execute_query retornó None o lista vacía")

except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Probar una vista de Django
print("\n6. Probando vistas de Django...")
try:
    import django
    django.setup()

    from myapp.views import lista_usuarios
    from django.test import RequestFactory

    factory = RequestFactory()
    request = factory.get('/usuarios/')

    response = lista_usuarios(request)
    print(f"   ✅ Vista lista_usuarios respondió con status: {response.status_code}")

except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("DIAGNÓSTICO COMPLETADO")
print("="*70)

