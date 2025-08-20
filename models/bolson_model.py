import sqlite3
from datetime import datetime
import os
import sys

class BolsonModel:
    def __init__(self, db_path=None):
        # Determinar la ruta correcta para la base de datos
        if getattr(sys, 'frozen', False):
            # Si estamos en un ejecutable
            application_path = os.path.dirname(sys.executable)
        else:
            # Si estamos en desarrollo
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        # Usar la ruta determinada para la base de datos
        self.db_path = os.path.join(application_path, 'bolsones.db') if db_path is None else db_path
        self._create_table()

    def _create_table(self):
        """Crea la tabla si no existe"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS registros_bolsones
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 proveedor TEXT,
                                 kilogramos TEXT,
                                 numero_lote TEXT,
                                 lote_adeco TEXT,
                                 numero_dit TEXT,
                                 reutilizable TEXT,
                                 fecha_registro TIMESTAMP,
                                 repeticiones INTEGER)''')
                conn.commit()
        except Exception as e:
            print(f"Error al crear tabla: {e}")
            # Intentar crear el directorio si no existe
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            # Intentar nuevamente
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS registros_bolsones
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 proveedor TEXT,
                                 kilogramos TEXT,
                                 numero_lote TEXT,
                                 lote_adeco TEXT,
                                 numero_dit TEXT,
                                 reutilizable TEXT,
                                 fecha_registro TIMESTAMP,
                                 repeticiones INTEGER)''')
                conn.commit()

    def guardar_registro(self, datos):
        """Guarda un nuevo registro en la base de datos"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO registros_bolsones 
                               (proveedor, kilogramos, numero_lote, lote_adeco, 
                                numero_dit, reutilizable, fecha_registro, repeticiones)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', datos)
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al guardar registro: {e}")
            return False

    def obtener_registros(self, filtros=None):
        """Obtiene registros con filtrado exacto"""
        query = "SELECT * FROM registros_bolsones"
        params = []
        
        if filtros:
            conditions = []
            if filtros.get('lote_adeco'):
                conditions.append("lote_adeco = ?")
                params.append(filtros['lote_adeco'])
            if filtros.get('proveedor'):
                if filtros.get('exact_match', False):
                    conditions.append("proveedor = ?")
                else:
                    conditions.append("proveedor LIKE ?")
                params.append(filtros['proveedor'])
                
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY fecha_registro DESC"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            return cursor.fetchall()

    def obtener_registro_por_id(self, registro_id):
        """Obtiene un registro específico por su ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM registros_bolsones WHERE id=?", (registro_id,))
            return cursor.fetchone()

    def actualizar_registro(self, registro_id, nuevos_datos):
        """Actualiza un registro existente"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''UPDATE registros_bolsones SET
                               proveedor=?, kilogramos=?, numero_lote=?, lote_adeco=?,
                               numero_dit=?, reutilizable=?, repeticiones=?
                               WHERE id=?''',
                               (*nuevos_datos, registro_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al actualizar registro: {e}")
            return False

    def eliminar_registro(self, registro_id):
        """Elimina un registro de la base de datos"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM registros_bolsones WHERE id=?', (registro_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al eliminar registro: {e}")
            return False