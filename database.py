import mysql.connector
from mysql.connector import Error
import traceback

class Database:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'usuarios_db'
        self.user = 'root'
        self.password = ''
        
    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                autocommit=False,
                pool_size=10,  # OPTIMIZACIÓN: Pool de conexiones
                pool_reset_session=True
            )
            return connection
        except Error as e:
            print(f"Error conectando a MySQL: {e}")
            return None
    
    def crear_tablas(self):
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Tabla de usuarios
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS usuarios (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nombre VARCHAR(50) NOT NULL,
                        apellido VARCHAR(50) NOT NULL,
                        edad INT NOT NULL,
                        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB
                """)
                
                # Tabla de correos
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS correos (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        usuario_id INT NOT NULL,
                        tipo VARCHAR(20) NOT NULL,
                        correo VARCHAR(100) NOT NULL,
                        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                        INDEX idx_usuario_tipo (usuario_id, tipo)
                    ) ENGINE=InnoDB
                """)
                
                connection.commit()
                print("✅ Tablas creadas/verificadas correctamente")
            except Error as e:
                print(f"Error creando tablas: {e}")
                connection.rollback()
            finally:
                if cursor:
                    cursor.close()
                connection.close()
    
    def guardar_correos_lote(self, correos):
        """OPTIMIZACIÓN: Inserta múltiples correos en un solo lote"""
        if not correos:
            return
        
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Preparar la consulta de inserción múltiple
                query = """
                    INSERT INTO correos (usuario_id, tipo, correo) 
                    VALUES (%s, %s, %s)
                """
                
                # Preparar los datos para inserción masiva
                datos = [
                    (correo['usuario_id'], correo['tipo'], correo['correo'])
                    for correo in correos
                ]
                
                # Ejecutar inserción masiva
                cursor.executemany(query, datos)
                connection.commit()
                
                print(f"✅ Insertados {len(correos)} correos en lote")
                
            except Error as e:
                print(f"Error en inserción masiva de correos: {e}")
                connection.rollback()
                # Fallback: insertar uno por uno si falla la inserción masiva
                self._guardar_correos_individualmente(correos)
            finally:
                if cursor:
                    cursor.close()
                connection.close()
    
    def _guardar_correos_individualmente(self, correos):
        """Fallback: Inserta correos uno por uno"""
        print("🔄 Usando inserción individual como fallback...")
        for correo in correos:
            self.guardar_correo(correo['usuario_id'], correo['tipo'], correo['correo'])
    
    def guardar_correo(self, usuario_id, tipo, correo):
        """Método original para inserción individual"""
        connection = self.get_connection()
        correo_id = None
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO correos (usuario_id, tipo, correo) VALUES (%s, %s, %s)",
                    (usuario_id, tipo, correo)
                )
                correo_id = cursor.lastrowid
                connection.commit()
            except Error as e:
                print(f"Error guardando correo: {e}")
                connection.rollback()
            finally:
                if cursor:
                    cursor.close()
                connection.close()
        return correo_id
    
    # ... (los demás métodos se mantienen igual)
    
    def obtener_usuarios(self):
        connection = self.get_connection()
        usuarios = []
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM usuarios ORDER BY id DESC")
                usuarios = cursor.fetchall()
            except Error as e:
                print(f"Error obteniendo usuarios: {e}")
            finally:
                if cursor:
                    cursor.close()
                connection.close()
        return usuarios
    
    def agregar_usuario(self, nombre, apellido, edad):
        connection = self.get_connection()
        usuario_id = None
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO usuarios (nombre, apellido, edad) VALUES (%s, %s, %s)",
                    (nombre, apellido, edad)
                )
                usuario_id = cursor.lastrowid
                connection.commit()
            except Error as e:
                print(f"Error agregando usuario: {e}")
                connection.rollback()
            finally:
                if cursor:
                    cursor.close()
                connection.close()
        return usuario_id
    
    def eliminar_usuario(self, usuario_id):
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
                connection.commit()
            except Error as e:
                print(f"Error eliminando usuario: {e}")
                connection.rollback()
            finally:
                if cursor:
                    cursor.close()
                connection.close()
    
    def eliminar_todos_usuarios(self):
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM usuarios")
                connection.commit()
            except Error as e:
                print(f"Error eliminando todos los usuarios: {e}")
                connection.rollback()
            finally:
                if cursor:
                    cursor.close()
                connection.close()
    
    def obtener_correos(self):
        connection = self.get_connection()
        correos = []
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("""
                    SELECT c.*, u.nombre, u.apellido 
                    FROM correos c 
                    JOIN usuarios u ON c.usuario_id = u.id 
                    ORDER BY c.id DESC
                """)
                correos = cursor.fetchall()
            except Error as e:
                print(f"Error obteniendo correos: {e}")
            finally:
                if cursor:
                    cursor.close()
                connection.close()
        return correos
    
    def eliminar_todos_correos(self):
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM correos")
                connection.commit()
            except Error as e:
                print(f"Error eliminando todos los correos: {e}")
                connection.rollback()
            finally:
                if cursor:
                    cursor.close()
                connection.close()