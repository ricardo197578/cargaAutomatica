from models.bolson_model import BolsonModel
import os

# Instancia global del modelo con manejo de rutas
db_model = BolsonModel()

def setup_database():
    """Inicializa la base de datos"""
    # Verificar si la base de datos existe
    if not os.path.exists(db_model.db_path):
        # Forzar la creación de la tabla
        db_model._create_table()

def guardar_registro(datos):
    """Función de conveniencia para el módulo views"""
    return db_model.guardar_registro(datos)

def obtener_registro_por_id(registro_id):
    """Obtiene un registro por su ID"""
    return db_model.obtener_registro_por_id(registro_id)

def actualizar_registro(registro_id, nuevos_datos):
    """Actualiza un registro existente"""
    return db_model.actualizar_registro(registro_id, nuevos_datos)

def eliminar_registro(registro_id):
    """Elimina un registro"""
    return db_model.eliminar_registro(registro_id)