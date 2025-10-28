"""
Configuración de conexión a Oracle sin ORM
Usando oracledb directamente (modo Thin - sin necesidad de Oracle Client)
Base de datos: Riffly Music Platform
"""
import oracledb
from datetime import datetime
import sys

# Configuración de la base de datos desde PyCharm
# Usuario: riffly_m
# Base de datos: localhost:1521/XE
DB_CONFIG = {
    'user': 'riffly_m',
    'password': 'root123',
    'host': 'localhost',
    'port': 1521,
    'service_name': 'XE'
}

def get_connection():
    """
    Obtener conexión a Oracle usando modo Thin (sin Oracle Client)
    """
    try:
        connection = oracledb.connect(
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            service_name=DB_CONFIG['service_name']
        )
        return connection
    except oracledb.Error as error:
        print(f"Error conectando a Oracle: {error}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        return None

def execute_query(query, params=None):
    """
    Ejecutar una consulta SELECT
    Retorna una lista de diccionarios con los resultados
    """
    connection = get_connection()
    if not connection:
        print("❌ No se pudo obtener conexión", file=sys.stderr)
        return []

    try:
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # Obtener nombres de columnas
        columns = [desc[0] for desc in cursor.description]

        # Obtener resultados como diccionarios
        results = []
        for row in cursor:
            row_dict = {}
            for i, col_name in enumerate(columns):
                row_dict[col_name] = row[i]
            results.append(row_dict)

        cursor.close()
        connection.close()
        return results

    except oracledb.Error as error:
        print(f"Error ejecutando query: {error}", file=sys.stderr)
        print(f"Query: {query}", file=sys.stderr)
        if connection:
            connection.close()
        return []
    except Exception as e:
        print(f"Error inesperado en execute_query: {e}", file=sys.stderr)
        if connection:
            connection.close()
        return []

def execute_dml(query, params=None):
    """
    Ejecutar INSERT, UPDATE, DELETE
    Retorna True si fue exitoso, False si hubo error
    """
    connection = get_connection()
    if not connection:
        print("❌ No se pudo obtener conexión", file=sys.stderr)
        return False

    try:
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        connection.close()
        return True

    except oracledb.Error as error:
        print(f"❌ Error ejecutando DML: {error}", file=sys.stderr)
        print(f"Query: {query}", file=sys.stderr)
        if connection:
            connection.rollback()
            connection.close()
        return False
    except Exception as e:
        print(f"Error inesperado en execute_dml: {e}", file=sys.stderr)
        if connection:
            connection.rollback()
            connection.close()
        return False

def execute_single(query, params=None):
    """
    Ejecutar una consulta que retorna un solo valor o fila
    """
    connection = get_connection()
    if not connection:
        print("❌ No se pudo obtener conexión", file=sys.stderr)
        return None

    try:
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        result = cursor.fetchone()

        if result and len(result) == 1:
            # Si es un solo valor, retornarlo directamente
            value = result[0]
        elif result:
            # Si es una fila completa, retornar como diccionario
            columns = [desc[0] for desc in cursor.description]
            value = dict(zip(columns, result))
        else:
            value = None

        cursor.close()
        connection.close()
        return value

    except oracledb.Error as error:
        print(f"Error ejecutando query single: {error}", file=sys.stderr)
        print(f"Query: {query}", file=sys.stderr)
        if connection:
            connection.close()
        return None
    except Exception as e:
        print(f"Error inesperado en execute_single: {e}", file=sys.stderr)
        if connection:
            connection.close()
        return None

def call_procedure(proc_name, params=None):
    """
    Llamar un procedimiento almacenado
    """
    connection = get_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor()
        if params:
            result = cursor.callproc(proc_name, params)
        else:
            result = cursor.callproc(proc_name)

        connection.commit()
        cursor.close()
        connection.close()
        return result

    except oracledb.Error as error:
        print(f"Error llamando procedimiento: {error}", file=sys.stderr)
        if connection:
            connection.rollback()
            connection.close()
        return None

def test_connection():
    """
    Probar la conexión a Oracle y mostrar estadísticas de la BD
    """
    print("🔍 Probando conexión a Oracle (Riffly Music Platform)...")
    print(f"   Usuario: {DB_CONFIG['user']}")
    print(f"   Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"   Service: {DB_CONFIG['service_name']}")
    print("-" * 50)

    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT 'Conexión exitosa!' FROM DUAL")
            result = cursor.fetchone()
            print(f"✅ {result[0]}")

            # Contar registros en cada tabla
            tablas = ['USERS', 'SONGS', 'GENRES', 'PLAYLISTS', 'COMMENTS', 'LIKES', 'PLAYS', 'FOLLOWS']
            print("\n📊 Estadísticas de la base de datos:")
            for tabla in tablas:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                    count = cursor.fetchone()[0]
                    print(f"   • {tabla}: {count} registros")
                except Exception as e:
                    print(f"   • {tabla}: (no accesible)")

            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            connection.close()
            return False
    else:
        print("❌ No se pudo establecer conexión")
        return False

if __name__ == "__main__":
    # Test cuando se ejecuta directamente
    test_connection()
