import mysql.connector
import sys

# --- CONFIGURACIÓN DE CONEXIÓN POR SWITCH ---
DB_HOST = "10.0.0.1"      # La IP estática de tu partición Linux
DB_USER = "admin_redes"   # El usuario de MySQL que creaste
DB_PASS = "tu_password_seguro" # Cambia esto si le pusiste otra contraseña
DB_NAME = "historia_mexico"
DB_PORT = 3306

PASSWORD_ADMIN = "Tragedias2026"  # Contraseña única compartida

def conectar():
    try:
        return mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME, port=DB_PORT
        )
    except mysql.connector.Error as err:
        print(f"❌ Error al conectar con el servidor Linux: {err}")
        sys.exit()

def verificar_admin():
    intento = input("🔒 Ingrese la contraseña de autorización: ")
    if intento == PASSWORD_ADMIN:
        return True
    else:
        print("❌ Contraseña incorrecta. Acceso denegado.\n")
        return False

def ingresar_desastre(db):
    if not verificar_admin(): return
    print("\n--- Ingresar Nuevo Registro ---")
    lugar = input("Lugar del suceso: ")
    fecha = input("Fecha (YYYY-MM-DD): ")
    hora = input("Hora (HH:MM): ")
    contexto = input("Contexto breve: ")
    
    cursor = db.cursor()
    sql = "INSERT INTO desastres (lugar, fecha, hora, contexto) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (lugar, fecha, hora, contexto))
    db.commit()
    print("✅ Registro guardado en el servidor.\n")

def revisar_lista(db):
    print("\n--- Lista de Desastres y Tragedias en México ---")
    cursor = db.cursor()
    cursor.execute("SELECT id, lugar, fecha, hora, contexto FROM desastres")
    resultados = cursor.fetchall()
    
    if not resultados:
        print("No hay registros en el servidor.\n")
        return

    for fila in resultados:
        print(f"ID: {fila[0]} | Lugar: {fila[1]} | Fecha: {fila[2]} | Hora: {fila[3]}")
        print(f"Contexto: {fila[4]}")
        print("-" * 50)
    print("")

def modificar_desastre(db):
    if not verificar_admin(): return
    revisar_lista(db)
    id_mod = input("Ingrese el ID del registro a modificar: ")
    
    print("Deje en blanco si no desea cambiar el campo.")
    nuevo_lugar = input("Nuevo lugar: ")
    nueva_fecha = input("Nueva fecha (YYYY-MM-DD): ")
    nueva_hora = input("Nueva hora (HH:MM): ")
    nuevo_contexto = input("Nuevo contexto: ")
    
    cursor = db.cursor()
    if nuevo_lugar: cursor.execute("UPDATE desastres SET lugar=%s WHERE id=%s", (nuevo_lugar, id_mod))
    if nueva_fecha: cursor.execute("UPDATE desastres SET fecha=%s WHERE id=%s", (nueva_fecha, id_mod))
    if nueva_hora: cursor.execute("UPDATE desastres SET hora=%s WHERE id=%s", (nueva_hora, id_mod))
    if nuevo_contexto: cursor.execute("UPDATE desastres SET contexto=%s WHERE id=%s", (nuevo_contexto, id_mod))
    
    db.commit()
    print("✅ Registro modificado en el servidor.\n")

def borrar_desastre(db):
    if not verificar_admin(): return
    revisar_lista(db)
    id_borrar = input("Ingrese el ID del registro a ELIMINAR: ")
    confirmacion = input("¿Confirmar eliminación? (s/n): ")
    
    if confirmacion.lower() == 's':
        cursor = db.cursor()
        cursor.execute("DELETE FROM desastres WHERE id=%s", (id_borrar,))
        db.commit()
        print("🗑️ Registro borrado permanentemente.\n")
    else:
        print("Operación cancelada.\n")

def mostrar_menu():
    db = conectar()
    while True:
        print("===== CONTROL DE REGISTROS HISTÓRICOS =====")
        print("1. Ingresar un desastre")
        print("2. Modificar un desastre")
        print("3. Revisar lista de desastres")
        print("4. Borrar un desastre")
        print("5. Salir")
        
        opcion = input("Seleccione una opción (1-5): ")
        
        if opcion == '1': ingresar_desastre(db)
        elif opcion == '2': modificar_desastre(db)
        elif opcion == '3': revisar_lista(db)
        elif opcion == '4': borrar_desastre(db)
        elif opcion == '5':
            print("Cerrando conexión con el servidor...")
            db.close()
            break
        else:
            print("Opción no válida. Intente de nuevo.\n")

# Esta línea es la que le dice a Python que arranque el menú interactivo
if __name__ == "__main__":
    mostrar_menu()