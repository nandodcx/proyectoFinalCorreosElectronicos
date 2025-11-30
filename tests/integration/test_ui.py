import unittest
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class TestCRMUI(unittest.TestCase):
    BASE_URL = "http://localhost:5000"
    
    def setUp(self):
        """Configuración antes de cada test"""
        print("\nConfigurando navegador para pruebas UI")
        
        # Configurar Chrome en modo headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
    
    def tearDown(self):
        """Limpieza después de cada test"""
        if self.driver:
            self.driver.quit()
    
    def test_1_homepage_load(self):
        """Test 1: Carga correcta de la página principal"""
        print("🧪 Test 1: Carga de página principal")
        
        self.driver.get(self.BASE_URL)
        
        # Verificar elementos clave
        self.assertIn("CRM Dashboard", self.driver.title)
        self.assertIn("Panel Principal", self.driver.page_source)
        
        # Verificar que se cargan las secciones principales
        dashboard_section = self.driver.find_element(By.ID, "dashboard")
        self.assertTrue(dashboard_section.is_displayed())
        
        print("✅ Página principal cargada correctamente")
    
    def test_2_navigation_flow(self):
        """Test 2: Navegación entre secciones"""
        print("🧪 Test 2: Navegación entre secciones")
        
        self.driver.get(self.BASE_URL)
        
        # Navegar a Usuarios
        users_link = self.driver.find_element(By.XPATH, "//a[.//p[text()='Usuarios']]")
        users_link.click()
        time.sleep(1)
        
        users_section = self.driver.find_element(By.ID, "users")
        self.assertFalse("hidden" in users_section.get_attribute("class").split())
        
        # Verificar que el título cambió
        page_title = self.driver.find_element(By.ID, "page-title")
        self.assertIn("Gestión de Usuarios", page_title.text)
        print("✅ Navegación a Usuarios funcionando")
        
        # Navegar a Correos
        emails_link = self.driver.find_element(By.XPATH, "//a[.//p[text()='Correos']]")
        emails_link.click()
        time.sleep(1)
        
        emails_section = self.driver.find_element(By.ID, "emails")
        self.assertFalse("hidden" in emails_section.get_attribute("class"))
        
        self.assertIn("Gestión de Correos", page_title.text)
        print("✅ Navegación a Correos funcionando")
        
        # Volver a Panel Principal
        dashboard_link = self.driver.find_element(By.XPATH, "//a[.//p[text()='Panel Principal']]")
        dashboard_link.click()
        time.sleep(1)
        
        self.assertIn("Panel Principal", page_title.text)
        print("✅ Navegación a Panel Principal funcionando")
    
    def test_3_user_creation_ui(self):
        """Test 3: Creación de usuario desde la UI"""
        print("🧪 Test 3: Creación de usuario UI")
        
        self.driver.get(self.BASE_URL)
        
        # Navegar a Usuarios
        users_link = self.driver.find_element(By.XPATH, "//a[.//p[text()='Usuarios']]")
        users_link.click()
        time.sleep(1)
        
        # Abrir formulario de agregar usuario
        add_user_btn = self.driver.find_element(By.ID, "btn-add-user")
        add_user_btn.click()
        time.sleep(0.5)
        
        # Verificar que el formulario se muestra
        user_form = self.driver.find_element(By.ID, "add-user-form")
        self.assertFalse("hidden" in user_form.get_attribute("class"))
        
        # Llenar formulario
        first_name = self.driver.find_element(By.ID, "user-firstname")
        first_name.send_keys("UITest")
        
        last_name = self.driver.find_element(By.ID, "user-lastname")
        last_name.send_keys("User")
        
        age = self.driver.find_element(By.ID, "user-age")
        age.send_keys("30")
        
        print("✅ Formulario de usuario completado")
    
    def test_4_dashboard_stats(self):
        """Test 4: Verificar estadísticas del dashboard"""
        print("🧪 Test 4: Estadísticas del dashboard")
        
        self.driver.get(self.BASE_URL)
        
        # Verificar que los contadores existen
        total_users = self.driver.find_element(By.ID, "total-users-count")
        total_emails = self.driver.find_element(By.ID, "total-emails-count")
        providers_count = self.driver.find_element(By.ID, "providers-count")
        
        self.assertTrue(total_users.is_displayed())
        self.assertTrue(total_emails.is_displayed())
        self.assertTrue(providers_count.is_displayed())
        
        print("✅ Contadores del dashboard mostrados correctamente")
    
    def test_5_buttons_functionality(self):
        """Test 5: Verificar que los botones existen y son clickeables"""
        print("🧪 Test 5: Funcionalidad de botones")
        
        self.driver.get(self.BASE_URL)
        
        # Verificar botones principales
        buttons_to_check = [
            "btn-generate-users",
            "btn-generate-emails", 
            "btn-mass-generate",
            "btn-clear-users",
            "btn-clear-emails"
        ]
        
        for btn_id in buttons_to_check:
            button = self.driver.find_element(By.ID, btn_id)
            self.assertTrue(button.is_displayed())
            self.assertTrue(button.is_enabled())
            print(f"✅ Botón {btn_id} está disponible")
        
        # Verificar campo de entrada
        mass_users_input = self.driver.find_element(By.ID, "mass-users-count")
        self.assertTrue(mass_users_input.is_displayed())
        self.assertTrue(mass_users_input.is_enabled())
        
        # Verificar que tiene un valor por defecto
        default_value = mass_users_input.get_attribute("value")
        self.assertIsNotNone(default_value)
        print("✅ Campo de entrada para usuarios masivos funcionando")

if __name__ == '__main__':
    print("INICIANDO PRUEBAS DE INTERFAZ DE USUARIO")
    print("=" * 60)
    print("Asegúrate de tener ChromeDriver instalado")
    unittest.main(verbosity=2)