#!/usr/bin/env python3
"""
Script para ejecutar todas las pruebas del proyecto CRM
"""

import subprocess
import sys
import os
import time

def print_header(message):
    print(f"\n{'='*60}")
    print(f"🚀 {message}")
    print(f"{'='*60}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def run_command(command, description, check_output=False):
    """Ejecutar comando y manejar resultados"""
    try:
        if check_output:
            result = subprocess.run(command, shell=True, check=True, 
                                  capture_output=True, text=True)
            return result.returncode == 0, result.stdout
        else:
            result = subprocess.run(command, shell=True, check=True)
            return result.returncode == 0, ""
    except subprocess.CalledProcessError as e:
        return False, str(e)

def check_server_health():
    """Verificar que el servidor esté funcionando"""
    import requests
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("🧪 INICIANDO SUITE COMPLETA DE PRUEBAS CRM")
    print("📋 Este script ejecutará todas las pruebas automatizadas")
    
    # Verificar salud del servidor
    print_header("VERIFICANDO SERVIDOR")
    if not check_server_health():
        print_error("El servidor Flask no está respondiendo en http://localhost:5000")
        print("💡 Ejecuta primero: python app.py")
        sys.exit(1)
    print_success("Servidor detectado y funcionando")
    
    tests_passed = 0
    tests_total = 0
    failed_tests = []
    
    # 1. Pruebas Unitarias
    print_header("EJECUTANDO PRUEBAS UNITARIAS")
    unit_tests = [
        ("python -m pytest tests/unit/test_models.py -v", "Pruebas de Modelos"),
        ("python -m pytest tests/unit/test_database.py -v", "Pruebas de Base de Datos"),
        ("python -m pytest tests/unit/test_app.py -v", "Pruebas de Aplicación")
    ]
    
    for command, description in unit_tests:
        success, output = run_command(command, description)
        if success:
            print_success(f"{description} - PASÓ")
            tests_passed += 1
        else:
            print_error(f"{description} - FALLÓ")
            failed_tests.append(description)
        tests_total += 1
        time.sleep(1)
    
    # 2. Pruebas de Integración
    print_header("EJECUTANDO PRUEBAS DE INTEGRACIÓN")
    integration_tests = [
        ("python tests/integration/test_api.py", "Pruebas de API"),
        ("python tests/integration/test_ui.py", "Pruebas de UI (Requiere ChromeDriver)")
    ]
    
    for command, description in integration_tests:
        success, output = run_command(command, description)
        if success:
            print_success(f"{description} - PASÓ")
            tests_passed += 1
        else:
            print_error(f"{description} - FALLÓ")
            failed_tests.append(description)
        tests_total += 1
        time.sleep(2)
    
    # 3. Pruebas de Rendimiento
    print_header("EJECUTANDO PRUEBAS DE RENDIMIENTO")
    success, output = run_command("python tests/performance/load_test.py", "Pruebas de Carga")
    if success:
        print_success("Pruebas de Rendimiento - PASÓ")
        tests_passed += 1
    else:
        print_error("Pruebas de Rendimiento - FALLÓ")
        failed_tests.append("Pruebas de Rendimiento")
    tests_total += 1
    
    # Resumen Final
    print_header("RESUMEN FINAL DE PRUEBAS")
    print(f"📊 Total de pruebas: {tests_total}")
    print(f"✅ Pruebas exitosas: {tests_passed}")
    print(f"❌ Pruebas fallidas: {tests_total - tests_passed}")
    print(f"📈 Porcentaje de éxito: {(tests_passed/tests_total)*100:.1f}%")
    
    if failed_tests:
        print(f"\n🔍 Pruebas que fallaron:")
        for test in failed_tests:
            print(f"   • {test}")
    
    if tests_passed == tests_total:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        print("🚀 El sistema está listo para producción")
        sys.exit(0)
    else:
        print(f"\n⚠️  {tests_total - tests_passed} prueba(s) fallaron")
        print("💡 Revisa los logs anteriores para más detalles")
        sys.exit(1)

if __name__ == "__main__":
    main()