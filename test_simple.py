import cx_Oracle

print("Probando conexión simple...")
try:
    conn = cx_Oracle.connect('riffly_m', 'root123', 'localhost:1521/XE')
    print("✅ CONEXIÓN EXITOSA")

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM USERS")
    count = cursor.fetchone()[0]
    print(f"Total usuarios: {count}")

    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ ERROR: {e}")

