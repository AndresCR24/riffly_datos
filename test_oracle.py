"""
Script para probar la conexión a Oracle antes de ejecutar Django
"""
import cx_Oracle

def test_oracle_connection():
    print("🔍 Probando conexión a Oracle...")
    print("-" * 50)

    # Configuración - Cambia estos valores por los tuyos
    config = {
        'user': 'tu_usuario',
        'password': 'tu_contraseña',
        'dsn': 'localhost:1521/XEPDB1'
    }

    try:
        # Intentar conectar
        connection = cx_Oracle.connect(
            user=config['user'],
            password=config['password'],
            dsn=config['dsn']
        )

        print("✅ ¡Conexión exitosa a Oracle!")
        print(f"📊 Versión de Oracle: {connection.version}")

        # Probar una consulta simple
        cursor = connection.cursor()
        cursor.execute("SELECT 'Hello from Oracle!' FROM DUAL")
        result = cursor.fetchone()
        print(f"📝 Resultado de prueba: {result[0]}")

        cursor.close()
        connection.close()
        print("\n✅ Todo funcionando correctamente!")

        return True

    except cx_Oracle.Error as error:
        print(f"❌ Error de conexión a Oracle:")
        print(f"   {error}")
        print("\n💡 Verifica:")
        print("   1. Oracle está corriendo")
        print("   2. Las credenciales son correctas")
        print("   3. El DSN/service name es correcto")
        print("   4. Oracle Instant Client está instalado")
        return False

    except ImportError:
        print("❌ cx_Oracle no está instalado")
        print("   Ejecuta: pip install cx_Oracle")
        return False


if __name__ == "__main__":
    test_oracle_connection()

