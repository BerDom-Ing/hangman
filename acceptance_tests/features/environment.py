from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import threading
import time
from app.web import app

def before_all(context):
    # Configurar Chrome para CI (headless)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    context.browser = webdriver.Chrome(options=chrome_options)
    
    # URL base (configurable por variable de entorno)
    context.base_url = os.getenv("BASE_URL", "http://localhost:5000")

def before_scenario(context, scenario):
    # Limpiar cookies/sesión antes de cada escenario
    if hasattr(context, 'browser'):
        context.browser.delete_all_cookies()
        # Navegar a la página de inicio para resetear estado
        context.browser.get(context.base_url)
        time.sleep(1)

def after_all(context):
    if hasattr(context, 'browser'):
        context.browser.quit()

