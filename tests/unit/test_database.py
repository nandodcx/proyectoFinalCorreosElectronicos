import sys
import os
import unittest
from unittest.mock import Mock, patch

# CORRECCIÓN: Agregar path correcto
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(parent_dir)
sys.path.insert(0, project_root)

try:
    from database import Database
    print("✅ Database importado correctamente")
except ImportError as e:
    print(f"❌ Error importando database: {e}")

class TestDatabase(unittest.TestCase):
    
    @patch('database.mysql.connector.connect')
    def test_get_connection_success(self, mock_connect):
        """Test de conexión exitosa a la base de datos"""
        # Configurar el mock
        mock_connection = Mock()
        mock_connect.return_value = mock_connection
        
        db = Database()
        connection = db.get_connection()
        
        # Verificar que se llamó a connect
        mock_connect.assert_called_once()
        self.assertEqual(connection, mock_connection)
        print("✅ Test conexión BD - PASÓ")
    
    def test_database_initialization(self):
        """Test de inicialización de la base de datos"""
        db = Database()
        self.assertEqual(db.host, 'localhost')
        self.assertEqual(db.database, 'usuarios_db')
        self.assertEqual(db.user, 'root')
        print("✅ Test inicialización BD - PASÓ")

if __name__ == '__main__':
    print("🧪 INICIANDO PRUEBAS DE BASE DE DATOS")
    print("=" * 50)
    unittest.main(verbosity=2)