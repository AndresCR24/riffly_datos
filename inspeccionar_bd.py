"""
Script para inspeccionar la estructura de la base de datos Oracle
y generar el código necesario
"""
import cx_Oracle

# Configuración - CAMBIA LA CONTRASEÑA
DB_CONFIG = {
    'user': 'riffly_m',
    'password': 'root123',  # CAMBIA ESTO
    'dsn': 'localhost:1521/XE',
    'encoding': 'UTF-8'
}

def inspeccionar_base_datos():
    """
    Inspecciona todas las tablas del usuario y su estructura
    """
    try:
        connection = cx_Oracle.connect(
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            dsn=DB_CONFIG['dsn'],
            encoding=DB_CONFIG['encoding']
        )

        cursor = connection.cursor()

        print("=" * 80)
        print("INSPECCIÓN DE BASE DE DATOS ORACLE")
        print(f"Usuario: {DB_CONFIG['user']}")
        print("=" * 80)
        print()

        # Obtener todas las tablas del usuario
        cursor.execute("""
            SELECT table_name 
            FROM user_tables 
            ORDER BY table_name
        """)

        tablas = cursor.fetchall()

        if not tablas:
            print("⚠️  No se encontraron tablas en la base de datos")
            print("   Asegúrate de que el usuario tenga tablas creadas")
            return

        print(f"📊 TABLAS ENCONTRADAS: {len(tablas)}")
        print("-" * 80)

        for (tabla_nombre,) in tablas:
            print(f"\n🔹 TABLA: {tabla_nombre}")
            print("-" * 80)

            # Obtener estructura de la tabla
            cursor.execute(f"""
                SELECT column_name, data_type, data_length, nullable, data_default
                FROM user_tab_columns
                WHERE table_name = '{tabla_nombre}'
                ORDER BY column_id
            """)

            columnas = cursor.fetchall()

            print(f"{'COLUMNA':<30} {'TIPO':<20} {'LONGITUD':<10} {'NULL':<8} {'DEFAULT'}")
            print("-" * 80)

            for col in columnas:
                col_name, data_type, data_length, nullable, data_default = col
                default = str(data_default)[:20] if data_default else ''
                print(f"{col_name:<30} {data_type:<20} {str(data_length):<10} {nullable:<8} {default}")

            # Obtener restricciones (primary key, foreign key, unique)
            cursor.execute(f"""
                SELECT constraint_name, constraint_type
                FROM user_constraints
                WHERE table_name = '{tabla_nombre}'
                AND constraint_type IN ('P', 'U', 'R')
                ORDER BY constraint_type
            """)

            restricciones = cursor.fetchall()

            if restricciones:
                print("\n  RESTRICCIONES:")
                for rest_name, rest_type in restricciones:
                    tipo_text = {'P': 'PRIMARY KEY', 'U': 'UNIQUE', 'R': 'FOREIGN KEY'}
                    print(f"    • {rest_name} ({tipo_text.get(rest_type, rest_type)})")

            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {tabla_nombre}")
            count = cursor.fetchone()[0]
            print(f"\n  📈 REGISTROS: {count}")

            # Mostrar primeros 2 registros de ejemplo
            if count > 0:
                cursor.execute(f"SELECT * FROM {tabla_nombre} WHERE ROWNUM <= 2")
                ejemplos = cursor.fetchall()
                col_names = [desc[0] for desc in cursor.description]

                print(f"\n  EJEMPLOS (primeros 2 registros):")
                for ejemplo in ejemplos:
                    print(f"    {dict(zip(col_names, ejemplo))}")

        print("\n" + "=" * 80)
        print("✅ INSPECCIÓN COMPLETADA")
        print("=" * 80)

        cursor.close()
        connection.close()

    except cx_Oracle.Error as error:
        print(f"❌ Error conectando a Oracle: {error}")
        print("\n💡 Verifica:")
        print("   1. La contraseña en este script es correcta")
        print("   2. Oracle está corriendo")
        print("   3. El usuario riffly_m existe")

if __name__ == "__main__":
    print("\n⚠️  IMPORTANTE: Configura tu contraseña en la línea 9 de este script")
    print("    'password': 'TU_CONTRASEÑA_AQUI'\n")

    respuesta = input("¿Ya configuraste la contraseña? (s/n): ")
    if respuesta.lower() == 's':
        inspeccionar_base_datos()
    else:
        print("\nPor favor configura la contraseña y vuelve a ejecutar el script.")

