import requests
import time
import threading
import statistics
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import os

class LoadTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.results = {
            'user_creation': [],
            'email_generation': [],
            'concurrent_operations': []
        }
    
    def test_single_user_creation(self, num_tests=5):
        """Test de creación individual de usuario"""
        print("🧪 Test de creación individual de usuarios")
        times = []
        
        for i in range(num_tests):
            start_time = time.time()
            
            try:
                response = requests.post(
                    f"{self.base_url}/usuarios",
                    json={
                        "nombre": f"LoadTest{i}",
                        "apellido": f"User{i}", 
                        "edad": 25 + i
                    },
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                end_time = time.time()
                response_time = end_time - start_time
                times.append(response_time)
                
                if response.status_code == 200:
                    user_id = response.json().get('id')
                    print(f"  ✅ Usuario {i+1}: {response_time:.3f}s (ID: {user_id})")
                else:
                    print(f"  ❌ Usuario {i+1}: Error {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Usuario {i+1}: Exception - {str(e)}")
        
        if times:
            avg_time = statistics.mean(times)
            max_time = max(times)
            min_time = min(times)
            
            self.results['user_creation'] = {
                'average': avg_time,
                'max': max_time,
                'min': min_time,
                'samples': len(times)
            }
            
            print(f"📊 Creación individual: Avg {avg_time:.3f}s, Max {max_time:.3f}s, Min {min_time:.3f}s")
        
        return times
    
    def test_batch_user_creation(self, batch_size=10):
        """Test de creación de usuarios en lote"""
        print(f"🧪 Test de creación en lote ({batch_size} usuarios)")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.base_url}/usuarios/aleatorios",
                json={"cantidad": batch_size},
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            
            end_time = time.time()
            batch_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                users_created = len(data.get('usuarios', []))
                time_per_user = batch_time / users_created if users_created > 0 else 0
                
                print(f"✅ Lote de {users_created} usuarios: {batch_time:.3f}s total")
                print(f"⏱️  Tiempo por usuario: {time_per_user:.3f}s")
                
                return batch_time, time_per_user
            else:
                print(f"❌ Error en creación por lote: {response.status_code}")
                return None, None
                
        except Exception as e:
            print(f"❌ Exception en creación por lote: {str(e)}")
            return None, None
    
    def test_email_generation_performance(self):
        """Test de rendimiento en generación de correos"""
        print("🧪 Test de generación de correos")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.base_url}/generar-correos",
                timeout=120
            )
            
            end_time = time.time()
            generation_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                emails_generated = len(data.get('correos', []))
                time_per_email = generation_time / emails_generated if emails_generated > 0 else 0
                
                self.results['email_generation'] = {
                    'total_time': generation_time,
                    'emails_count': emails_generated,
                    'time_per_email': time_per_email
                }
                
                print(f"✅ {emails_generated} correos generados en {generation_time:.3f}s")
                print(f"⏱️  Tiempo por correo: {time_per_email:.3f}s")
                
                return generation_time, emails_generated
            else:
                print(f"❌ Error en generación de correos: {response.status_code}")
                return None, None
                
        except Exception as e:
            print(f"❌ Exception en generación de correos: {str(e)}")
            return None, None
    
    def test_concurrent_operations(self, num_concurrent=5):
        """Test de operaciones concurrentes"""
        print(f"🧪 Test de operaciones concurrentes ({num_concurrent} usuarios)")
        
        def create_user(user_id):
            try:
                start_time = time.time()
                
                response = requests.post(
                    f"{self.base_url}/usuarios",
                    json={
                        "nombre": f"Concurrent{user_id}",
                        "apellido": f"Test{user_id}", 
                        "edad": 20 + user_id
                    },
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                end_time = time.time()
                
                if response.status_code == 200:
                    return end_time - start_time, response.json().get('id')
                else:
                    return None, None
                    
            except Exception as e:
                return None, None
        
        times = []
        user_ids = []
        
        with ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            future_to_user = {executor.submit(create_user, i): i for i in range(num_concurrent)}
            
            for future in as_completed(future_to_user):
                result = future.result()
                if result[0] is not None:
                    times.append(result[0])
                    user_ids.append(result[1])
        
        if times:
            avg_time = statistics.mean(times)
            max_time = max(times)
            min_time = min(times)
            
            self.results['concurrent_operations'] = {
                'average': avg_time,
                'max': max_time,
                'min': min_time,
                'successful_requests': len(times),
                'total_requests': num_concurrent
            }
            
            success_rate = (len(times) / num_concurrent) * 100
            
            print(f"📊 Operaciones concurrentes:")
            print(f"  ✅ Solicitudes exitosas: {len(times)}/{num_concurrent} ({success_rate:.1f}%)")
            print(f"  ⏱️  Tiempo promedio: {avg_time:.3f}s")
            print(f"  📈 Tiempo máximo: {max_time:.3f}s")
            print(f"  📉 Tiempo mínimo: {min_time:.3f}s")
        
        # Limpiar usuarios creados
        for user_id in user_ids:
            try:
                requests.delete(f"{self.base_url}/usuarios/{user_id}")
            except:
                pass
        
        return times
    
    def run_comprehensive_test(self):
        """Ejecutar suite completa de pruebas de rendimiento"""
        print("🚀 INICIANDO PRUEBAS COMPLETAS DE RENDIMIENTO")
        print("=" * 60)
        
        # 1. Creación individual de usuarios
        self.test_single_user_creation(5)
        print("-" * 40)
        
        # 2. Creación por lotes
        self.test_batch_user_creation(10)
        print("-" * 40)
        
        # 3. Generación de correos
        self.test_email_generation_performance()
        print("-" * 40)
        
        # 4. Operaciones concurrentes
        self.test_concurrent_operations(5)
        print("-" * 40)
        
        # Mostrar resumen
        self.print_summary()
    
    def print_summary(self):
        """Imprimir resumen de resultados"""
        print("\n📊 RESUMEN DE RENDIMIENTO")
        print("=" * 60)
        
        if self.results['user_creation']:
            data = self.results['user_creation']
            print(f"👤 Creación individual de usuarios:")
            print(f"   • Muestras: {data['samples']}")
            print(f"   • Tiempo promedio: {data['average']:.3f}s")
            print(f"   • Rango: {data['min']:.3f}s - {data['max']:.3f}s")
        
        if self.results['email_generation']:
            data = self.results['email_generation']
            print(f"📧 Generación de correos:")
            print(f"   • Total correos: {data['emails_count']}")
            print(f"   • Tiempo total: {data['total_time']:.3f}s")
            print(f"   • Tiempo/correo: {data['time_per_email']:.3f}s")
        
        if self.results['concurrent_operations']:
            data = self.results['concurrent_operations']
            success_rate = (data['successful_requests'] / data['total_requests']) * 100
            print(f"🔀 Operaciones concurrentes:")
            print(f"   • Tasa de éxito: {success_rate:.1f}%")
            print(f"   • Tiempo promedio: {data['average']:.3f}s")

if __name__ == "__main__":
    tester = LoadTester()
    tester.run_comprehensive_test()