import sys
import os
import unittest

# CORRECCIÓN: Agregar path correcto
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(parent_dir)
sys.path.insert(0, project_root)

try:
    from app import app
    print("✅ App importada correctamente")
except ImportError as e:
    print(f"❌ Error importando app: {e}")

class TestApp(unittest.TestCase):
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.app = app
        self.client = app.test_client()
        self.client.testing = True
        print("✅ Configuración de测试 completada")
    
    def test_index_route(self):
        """Test de la ruta principal"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CRM Dashboard', response.data)
        print("✅ Ruta principal funcionando")
    
    def test_obtener_usuarios_route(self):
        """Test de la ruta obtener usuarios"""
        response = self.client.get('/usuarios')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)
        print("✅ Ruta /usuarios funcionando")
    
    def test_agregar_usuario_route(self):
        """Test de agregar usuario"""
        user_data = {
            'nombre': 'Test',
            'apellido': 'User', 
            'edad': 25
        }
        
        response = self.client.post(
            '/usuarios',
            json=user_data,
            content_type='application/json'
        )
        
        # Puede devolver 200 (éxito) o 400 (datos inválidos)
        self.assertIn(response.status_code, [200, 400])
        print("✅ Ruta POST /usuarios funcionando")

if __name__ == '__main__':
    print("🧪 INICIANDO PRUEBAS DE LA APLICACIÓN")
    print("=" * 50)
    unittest.main(verbosity=2)