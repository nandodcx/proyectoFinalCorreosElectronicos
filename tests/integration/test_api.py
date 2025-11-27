import requests
import json
import unittest
import time
import sys
import os

class TestCRMAPIIntegration(unittest.TestCase):
    BASE_URL = "http://localhost:5000"
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.session = requests.Session()
        self.test_users = []
        print(f"\n🔗 Configurando prueba en: {self.BASE_URL}")
    
    def tearDown(self):
        """Limpieza después de cada test"""
        # Limpiar usuarios de prueba si existen
        for user_id in self.test_users:
            try:
                self.session.delete(f"{self.BASE_URL}/usuarios/{user_id}")
            except:
                pass
    
    def test_1_api_health_check(self):
        """Test 1: Verificar que la API está funcionando"""
        print("🧪 Test 1: Health Check")
        response = self.session.get(f"{self.BASE_URL}/")
        self.assertEqual(response.status_code, 200)
        print("✅ API está funcionando correctamente")
    
    def test_2_crud_usuario_flow(self):
        """Test 2: Flujo completo CRUD de usuario"""
        print("🧪 Test 2: Flujo CRUD Usuario")
        
        # Crear usuario
        user_data = {
            "nombre": "Integration",
            "apellido": "Test", 
            "edad": 28
        }
        
        response = self.session.post(
            f"{self.BASE_URL}/usuarios",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('id', data)
        user_id = data['id']
        self.test_users.append(user_id)
        print(f"✅ Usuario creado con ID: {user_id}")
        
        # Verificar que aparece en la lista
        response = self.session.get(f"{self.BASE_URL}/usuarios")
        self.assertEqual(response.status_code, 200)
        users = response.json()
        self.assertIsInstance(users, list)
        
        user_found = any(u['id'] == user_id for u in users)
        self.assertTrue(user_found, "Usuario creado no encontrado en la lista")
        print("✅ Usuario encontrado en la lista")
        
        # Eliminar usuario
        response = self.session.delete(f"{self.BASE_URL}/usuarios/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.test_users.remove(user_id)
        print("✅ Usuario eliminado correctamente")
    
    def test_3_generate_random_users(self):
        """Test 3: Generación de usuarios aleatorios"""
        print("🧪 Test 3: Generación usuarios aleatorios")
        
        response = self.session.post(
            f"{self.BASE_URL}/usuarios/aleatorios",
            json={"cantidad": 5},
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('usuarios', data)
        self.assertEqual(len(data['usuarios']), 5)
        
        # Guardar IDs para limpieza
        for user in data['usuarios']:
            self.test_users.append(user['id'])
        
        print(f"✅ Generados {len(data['usuarios'])} usuarios aleatorios")
    
    def test_4_email_generation_flow(self):
        """Test 4: Flujo completo de generación de correos"""
        print("🧪 Test 4: Generación de correos")
        
        # Primero crear un usuario
        user_data = {
            "nombre": "Email",
            "apellido": "Generator", 
            "edad": 32
        }
        
        response = self.session.post(
            f"{self.BASE_URL}/usuarios",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )
        
        user_id = response.json()['id']
        self.test_users.append(user_id)
        print(f"✅ Usuario para correos creado: {user_id}")
        
        # Generar correos
        start_time = time.time()
        response = self.session.post(f"{self.BASE_URL}/generar-correos")
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn('correos', data)
        self.assertIn('tiempo', data)
        self.assertGreater(len(data['correos']), 0)
        
        generation_time = end_time - start_time
        print(f"✅ Generados {len(data['correos'])} correos en {data['tiempo']:.2f}s")
        print(f"⏱️  Tiempo real: {generation_time:.2f}s")
        
        # Verificar que los correos están en la lista
        response = self.session.get(f"{self.BASE_URL}/correos")
        self.assertEqual(response.status_code, 200)
        emails = response.json()
        self.assertIsInstance(emails, list)
        print(f"✅ Total de correos en sistema: {len(emails)}")
    
    def test_5_mass_operations(self):
        """Test 5: Operaciones masivas"""
        print("🧪 Test 5: Operaciones masivas")
        
        # Generar múltiples usuarios
        response = self.session.post(
            f"{self.BASE_URL}/usuarios/aleatorios",
            json={"cantidad": 10},
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.status_code, 200)
        users_data = response.json()
        
        # Guardar IDs
        for user in users_data['usuarios']:
            self.test_users.append(user['id'])
        
        print(f"✅ Generados {len(users_data['usuarios'])} usuarios para prueba masiva")
        
        # Generar correos para todos
        response = self.session.post(f"{self.BASE_URL}/generar-correos")
        self.assertEqual(response.status_code, 200)
        emails_data = response.json()
        
        print(f"✅ Generados {len(emails_data['correos'])} correos en operación masiva")
        
        # Verificar estadísticas
        response = self.session.get(f"{self.BASE_URL}/usuarios")
        users_count = len(response.json())
        
        response = self.session.get(f"{self.BASE_URL}/correos")
        emails_count = len(response.json())
        
        print(f"📊 Estadísticas finales - Usuarios: {users_count}, Correos: {emails_count}")

if __name__ == '__main__':
    print("🚀 INICIANDO PRUEBAS DE INTEGRACIÓN API")
    print("=" * 60)
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor detectado, iniciando pruebas...")
            unittest.main(verbosity=2)
        else:
            print("❌ Servidor no responde correctamente")
    except requests.ConnectionError:
        print("❌ No se puede conectar al servidor en http://localhost:5000")
        print("💡 Asegúrate de que el servidor Flask esté ejecutándose")