import sys
import os
import unittest
from datetime import datetime

# Agregar el directorio raíz al path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(parent_dir)
sys.path.insert(0, project_root)

from models import Usuario, Correo

class TestModels(unittest.TestCase):
    
    def test_usuario_creation_basic(self):
        """Test creación básica de usuario"""
        usuario = Usuario(1, "Juan", "Pérez", 30)
        self.assertEqual(usuario.id, 1)
        self.assertEqual(usuario.nombre, "Juan")
        self.assertEqual(usuario.apellido, "Pérez")
        self.assertEqual(usuario.edad, 30)
        self.assertIsNone(usuario.fecha_creacion)
        print("✅ Test usuario creación básica - PASÓ")
    
    def test_usuario_creation_with_date(self):
        """Test creación de usuario con fecha"""
        fecha = datetime.now()
        usuario = Usuario(2, "Maria", "Gomez", 25, fecha)
        self.assertEqual(usuario.fecha_creacion, fecha)
        print("✅ Test usuario con fecha - PASÓ")
    
    def test_usuario_to_dict(self):
        """Test conversión a diccionario"""
        usuario = Usuario(1, "Carlos", "Lopez", 35)
        usuario_dict = usuario.to_dict()
        
        expected_keys = ['id', 'nombre', 'apellido', 'edad', 'fecha_creacion']
        for key in expected_keys:
            self.assertIn(key, usuario_dict)
        
        self.assertEqual(usuario_dict['nombre'], "Carlos")
        self.assertEqual(usuario_dict['apellido'], "Lopez")
        self.assertEqual(usuario_dict['edad'], 35)
        print("✅ Test usuario to_dict - PASÓ")
    
    def test_correo_creation_basic(self):
        """Test creación básica de correo"""
        correo = Correo(1, 100, "gmail", "test@gmail.com")
        self.assertEqual(correo.id, 1)
        self.assertEqual(correo.usuario_id, 100)
        self.assertEqual(correo.tipo, "gmail")
        self.assertEqual(correo.correo, "test@gmail.com")
        self.assertIsNone(correo.fecha_creacion)
        self.assertIsNone(correo.nombre)
        self.assertIsNone(correo.apellido)
        print("✅ Test correo creación básica - PASÓ")
    
    def test_correo_creation_complete(self):
        """Test creación completa de correo"""
        correo = Correo(
            id=1, 
            usuario_id=100, 
            tipo="outlook", 
            correo="test@outlook.com",
            fecha_creacion=datetime.now(),
            nombre="Ana",
            apellido="Ruiz"
        )
        
        self.assertEqual(correo.tipo, "outlook")
        self.assertEqual(correo.nombre, "Ana")
        self.assertEqual(correo.apellido, "Ruiz")
        self.assertIsNotNone(correo.fecha_creacion)
        print("✅ Test correo creación completa - PASÓ")
    
    def test_correo_to_dict(self):
        """Test conversión de correo a diccionario"""
        correo = Correo(1, 100, "empresa", "test@empresa.com")
        correo_dict = correo.to_dict()
        
        expected_keys = ['id', 'usuario_id', 'tipo', 'correo', 'fecha_creacion', 'nombre', 'apellido']
        for key in expected_keys:
            self.assertIn(key, correo_dict)
        
        self.assertEqual(correo_dict['tipo'], "empresa")
        self.assertEqual(correo_dict['correo'], "test@empresa.com")
        print("✅ Test correo to_dict - PASÓ")

if __name__ == '__main__':
    print("🧪 INICIANDO PRUEBAS DE MODELOS")
    print("=" * 50)
    unittest.main(verbosity=2)
