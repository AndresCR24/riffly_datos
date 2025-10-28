#!/usr/bin/env python3
"""Script de prueba de conexión a Oracle"""

print("=" * 60)
print("PRUEBA DE CONEXIÓN A ORACLE")
print("=" * 60)

# 1. Verificar oracledb
try:
    import oracledb
    print("✅ oracledb instalado - version:", oracledb.__version__)
except ImportError:
    print("❌ oracledb NO instalado")
    print("   Ejecuta: pip install oracledb")
    exit(1)

# 2. Intentar conexión
print("\n🔍 Intentando conectar a Oracle...")
print("   Host: localhost:1521")
print("   Service: XE")
print("   Usuario: riffly_m")

try:
    conn = oracledb.connect(
        user='riffly_m',
        password='root123',
        host='localhost',
        port=1521,
        service_name='XE'
    )
    print("✅ ¡CONEXIÓN EXITOSA!")

    # 3. Probar consulta simple
    print("\n📊 Consultando base de datos...")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM USERS")
    users_count = cursor.fetchone()[0]
    print(f"   • USERS: {users_count} registros")

    cursor.execute("SELECT COUNT(*) FROM SONGS")
    songs_count = cursor.fetchone()[0]
    print(f"   • SONGS: {songs_count} registros")

    cursor.execute("SELECT COUNT(*) FROM GENRES")
    genres_count = cursor.fetchone()[0]
    print(f"   • GENRES: {genres_count} registros")

    cursor.close()
    conn.close()

    print("\n" + "=" * 60)
    print("✅ TODO FUNCIONA CORRECTAMENTE")
    print("=" * 60)

except oracledb.Error as e:
    print(f"\n❌ ERROR DE ORACLE: {e}")
    print("\nPosibles soluciones:")
    print("   1. Verifica que el contenedor Docker esté corriendo:")
    print("      docker ps | grep oracle")
    print("   2. Verifica las credenciales en db_connection.py")
    print("   3. Verifica que el usuario riffly_m existe en la BD")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

