#!/usr/bin/env python3
"""Prueba específica de comentarios"""

import sys
sys.path.insert(0, '/Users/andresdavidcardenasramirez/Desktop/DjangoProject')

from db_connection import execute_query, execute_single

print("=" * 60)
print("PRUEBA DE COMENTARIOS")
print("=" * 60)

# 1. Verificar si la tabla COMMENTS existe
print("\n1️⃣ Verificando tabla COMMENTS...")
try:
    count = execute_single("SELECT COUNT(*) FROM COMMENTS")
    print(f"✅ Tabla COMMENTS existe: {count} registros")
except Exception as e:
    print(f"❌ Error: {e}")

# 2. Probar la consulta completa de comentarios
print("\n2️⃣ Probando consulta completa...")
query = """
    SELECT c.COMMENT_ID, c.BODY, c.CREATED_AT,
           u.USERNAME, u.DISPLAY_NAME,
           s.TITLE as SONG_TITLE, s.SONG_ID
    FROM COMMENTS c
    JOIN USERS u ON c.USER_ID = u.USER_ID
    JOIN SONGS s ON c.SONG_ID = s.SONG_ID
    WHERE c.IS_DELETED = 'N'
    ORDER BY c.CREATED_AT DESC
    FETCH FIRST 5 ROWS ONLY
"""

comentarios = execute_query(query)
print(f"✅ Consulta exitosa: {len(comentarios)} comentarios encontrados")

if comentarios:
    print("\n📝 Primeros comentarios:")
    for i, com in enumerate(comentarios[:3], 1):
        print(f"   {i}. {com.get('USERNAME')}: {com.get('BODY')[:50]}...")
else:
    print("⚠️ No hay comentarios en la base de datos")

# 3. Verificar estructura de la tabla
print("\n3️⃣ Verificando estructura de COMMENTS...")
query_estructura = """
    SELECT COLUMN_NAME, DATA_TYPE 
    FROM USER_TAB_COLUMNS 
    WHERE TABLE_NAME = 'COMMENTS'
    ORDER BY COLUMN_ID
"""
columnas = execute_query(query_estructura)
if columnas:
    print("✅ Columnas de la tabla COMMENTS:")
    for col in columnas:
        print(f"   • {col['COLUMN_NAME']}: {col['DATA_TYPE']}")

print("\n" + "=" * 60)

