from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time
from app.web import app

# Flask app para tests
def start_flask_app():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(port=5000)

def before_all(context):
    # Configurar y iniciar la app Flask en un thread separado
    context.server_thread = threading.Thread(target=start_flask_app)
    context.server_thread.daemon = True
    context.server_thread.start()
    time.sleep(1)  # Esperar a que el servidor esté listo
    
    # Configurar el driver de Selenium
    service = Service(ChromeDriverManager().install())
    context.browser = webdriver.Chrome(service=service)
    context.browser.implicitly_wait(10)
    context.base_url = "http://localhost:5000"
    
    # Variables para mock de pruebas
    context.test_word = None

def after_all(context):
    context.browser.quit()
    # No es necesario detener el thread del servidor Flask, ya que es un daemon

def before_scenario(context, scenario):
    # Limpiar cookies/sesión entre escenarios
    context.browser.delete_all_cookies()