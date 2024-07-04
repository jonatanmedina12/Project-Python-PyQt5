import os
import random
import sqlite3
import sys
from datetime import datetime, timedelta


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class sqlConfiguration:
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def create_connection(self):
        conn = None
        try:
            config_db_path = resource_path(os.path.join('internal', 'config.db'))
            os.makedirs(os.path.dirname(config_db_path), exist_ok=True)
            conn = sqlite3.connect(f'file:{config_db_path}?mode=rwc&user={self.user}&password={self.password}',
                                   uri=True)
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        return conn

    @staticmethod
    def create_table(conn):
        try:
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS configuration
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, main_endpoint TEXT, methods TEXT, functions TEXT)""")
            conn.commit()
        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def save_configuration(conn, main_endpoint, methods, functions):
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM configuration")
            row = c.fetchone()

            methods_str = ", ".join(methods)
            functions_str = ", ".join(functions)

            print("Guardando configuración:")
            print(f"Main Endpoint: {main_endpoint}")
            print(f"Methods: {methods_str}")
            print(f"Functions: {functions_str}")

            if row:
                # Actualizar la configuración existente
                c.execute("UPDATE configuration SET main_endpoint=?, methods=?, functions=?",
                          (main_endpoint, methods_str, functions_str))
                print("Actualizando configuración existente")
            else:
                # Insertar una nueva configuración
                c.execute("INSERT INTO configuration (main_endpoint, methods, functions) VALUES (?, ?, ?)",
                          (main_endpoint, methods_str, functions_str))
                print("Insertando nueva configuración")

            conn.commit()
            print("Configuración guardada exitosamente")
        except sqlite3.Error as e:
            print("Error al guardar la configuración:", e)

    @staticmethod
    def load_configuration(conn):
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM configuration")
            row = c.fetchone()

            print(f"Fila recuperada de la base de datos: {row}")

            if row:
                main_endpoint = row[1]
                methods = row[2].split(", ") if row[2] else []
                functions = row[3].split(", ") if row[3] else []
                print(f"Datos cargados de la base de datos:")
                print(f"Main Endpoint: {main_endpoint}")
                print(f"Methods: {methods}")
                print(f"Functions: {functions}")
                return main_endpoint, methods, functions
            else:
                print("No se encontraron datos en la tabla de configuración")
                return None, None, None
        except sqlite3.Error as e:
            print("Error al cargar la configuración:", e)
            return None, None, None

    @staticmethod
    def create_parametrization_table(conn):
        try:
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS parametrization
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                          usuario TEXT,
                          contrasena TEXT,
                          nombre_equipo TEXT,
                          tipo_conexion TEXT,
                          direccion TEXT,
                          ip TEXT,
                          socket1 TEXT,
                          funcion_socket1 TEXT,
                          tipo_socket1 TEXT,
                          socket2 TEXT,
                          funcion_socket2 TEXT,
                          tipo_socket2 TEXT,
                          modo_socket TEXT,
                          puerto TEXT,
                          baudios TEXT,
                          bits_datos TEXT,
                          paridad TEXT,
                          bits_parada TEXT)""")
            conn.commit()
        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def save_parametrization(conn, params):
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM parametrization")
            row = c.fetchone()

            if row:
                # Actualizar la parametrización existente
                c.execute("""UPDATE parametrization SET 
                              usuario=?, contrasena=?, nombre_equipo=?, tipo_conexion=?,
                              direccion=?, ip=?, socket1=?, funcion_socket1=?, tipo_socket1=?,
                              socket2=?, funcion_socket2=?, tipo_socket2=?, modo_socket=?,
                              puerto=?, baudios=?, bits_datos=?, paridad=?, bits_parada=?
                              WHERE id=1""", params)
            else:
                # Insertar una nueva parametrización
                c.execute("""INSERT INTO parametrization 
                              (usuario, contrasena, nombre_equipo, tipo_conexion,
                              direccion, ip, socket1, funcion_socket1, tipo_socket1,
                              socket2, funcion_socket2, tipo_socket2, modo_socket,
                              puerto, baudios, bits_datos, paridad, bits_parada)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", params)

            conn.commit()
        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def load_parametrization(conn):
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM parametrization")
            row = c.fetchone()

            if row:
                return row[1:]  # Devuelve todos los campos excepto el id
            else:
                return None
        except sqlite3.Error as e:
            print(e)
            return None

    @staticmethod
    def create_analyzer_table(conn):
        try:
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS analyzer
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                is_selected INTEGER)""")
            conn.commit()
        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def save_analyzers(conn, analyzers):
        try:
            c = conn.cursor()
            c.execute("DELETE FROM analyzer")  # Limpiar la tabla existente
            for analyzer in analyzers:
                c.execute("INSERT INTO analyzer (name, is_selected) VALUES (?, 0)", (analyzer,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def load_analyzers(conn):
        try:
            c = conn.cursor()
            c.execute("SELECT name FROM analyzer")
            return [row[0] for row in c.fetchall()]
        except sqlite3.Error as e:
            print(e)
            return []

    @staticmethod
    def save_selected_analyzer(conn, analyzer_name):
        try:
            c = conn.cursor()
            c.execute("UPDATE analyzer SET is_selected = 0")  # Resetear todas las selecciones
            c.execute("UPDATE analyzer SET is_selected = 1 WHERE name = ?", (analyzer_name,))
            conn.commit()
        except sqlite3.Error as e:
            print(e)

    @staticmethod
    def load_selected_analyzer(conn):
        try:
            c = conn.cursor()
            c.execute("SELECT name FROM analyzer WHERE is_selected = 1")
            row = c.fetchone()
            return row[0] if row else None
        except sqlite3.Error as e:
            print(e)
            return None

    @staticmethod
    def create_history_table(conn):
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS history
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         date TEXT,
         action TEXT,
         details TEXT,
         details_observer TEXT)
        ''')
        conn.commit()

    @staticmethod
    def load_history(conn, limit, offset, search_text, date_from, date_to):
        try:
            cursor = conn.cursor()
            query = "SELECT date, action, details, details_observer FROM history WHERE date >= ? AND date < ?"
            params = [date_from, date_to]
            print(query)
            if search_text:
                query += " AND (action LIKE ? OR details LIKE ? OR details_observer LIKE ?)"
                params.extend(['%' + search_text + '%'] * 3)

            query += " ORDER BY date DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])

            print("Query:", query)
            print("Params:", params)

            cursor.execute(query, params)
            history_entries = cursor.fetchall()
            print(history_entries)
            return history_entries
        except Exception as e:
            print(f"Error al cargar el historial: {e}")
            return []

    @staticmethod
    def add_to_history(conn, action, details):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history (date, action, details) VALUES (datetime('now'), ?, ?)", (action, details))
        conn.commit()

    @staticmethod
    def insert_test_data(conn):
        # Lista de acciones posibles
        actions = [
            "Inicio de sesión",
            "Cierre de sesión",
            "Modificación de configuración",
            "Ejecución de análisis",
            "Exportación de datos",
            "Importación de datos",
            "Creación de usuario",
            "Eliminación de usuario",
            "Actualización de software",
            "Backup de base de datos"
        ]

        # Lista de detalles posibles
        details = [
            "Usuario: admin",
            "Usuario: operador1",
            "Usuario: analista2",
            "Módulo: Configuración general",
            "Módulo: Análisis de muestras",
            "Módulo: Gestión de usuarios",
            "Archivo: datos_2023.csv",
            "Versión: 2.1.3",
            "Base de datos: principal",
            "Duración: 5 minutos"
        ]

        # Trama completa
        full_trama = (
            ""
        )

        # Generar y insertar 100 entradas de prueba
        for i in range(100):
            # Generar una fecha aleatoria en los últimos 30 días
            random_date = datetime.now() - timedelta(days=random.randint(0, 30))
            action = random.choice(actions)
            detail = random.choice(details)

            # Insertar en la base de datos
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO history (date, action, details, details_observer) VALUES (?, ?, ?, ?)",
                (random_date.strftime("%Y-%m-%d %H:%M:%S"), action, detail, full_trama)
            )

        conn.commit()
        print("Datos de prueba insertados con éxito.")
