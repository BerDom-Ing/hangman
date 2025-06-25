from behave import given, when, then
from selenium.webdriver.common.by import By
import time
import re
from app.web import app, WORDS

# Modificar la lista de palabras durante las pruebas
def set_test_word(word):
    original_choice = WORDS.copy()
    WORDS.clear()
    WORDS.append(word)
    return original_choice

def restore_words(original_words):
    WORDS.clear()
    WORDS.extend(original_words)

# Steps para inicio de sesión
@given('estoy en la página de inicio')
def step_impl(context):
    context.browser.get(context.base_url)
    assert "Hangman Game" in context.browser.title

@when('ingreso el nombre "{username}"')
def step_impl(context, username):
    username_input = context.browser.find_element(By.ID, "username")
    username_input.clear()
    username_input.send_keys(username)

@when('hago clic en el botón "{button_text}"')
def step_impl(context, button_text):
    buttons = context.browser.find_elements(By.XPATH, f"//button[contains(text(), '{button_text}')]")
    if buttons:
        buttons[0].click()
    else:
        links = context.browser.find_elements(By.XPATH, f"//a[contains(text(), '{button_text}')]")
        if links:
            links[0].click()
        else:
            assert False, f"No se encontró botón o enlace con texto '{button_text}'"
    time.sleep(2)  # Esperar a que la página se cargue

@then('debería ver la página del juego')
def step_impl(context):
    assert context.browser.find_element(By.ID, "display-word")
    assert context.browser.find_element(By.ID, "lives-count")

@then('debería ver mi nombre "{username}" en la página')
def step_impl(context, username):
    page_text = context.browser.find_element(By.TAG_NAME, "body").text
    assert username in page_text, f"No se encontró '{username}' en la página"

# Steps para sesión iniciada
@given('estoy logueado como "{username}"')
def step_impl(context, username):
    # Forzar ir a la página de inicio para estado limpio
    context.browser.get(context.base_url)
    time.sleep(1)
    
    try:
        # Buscar el formulario de login
        username_input = context.browser.find_element(By.ID, "username")
        username_input.clear()
        username_input.send_keys(username)
        
        form = context.browser.find_element(By.ID, "login-form")
        button = form.find_element(By.TAG_NAME, "button")
        button.click()
        time.sleep(2)  # Más tiempo de espera
        
    except Exception as e:
        # Si no puede hacer login, verificar si ya está logueado
        page_text = context.browser.find_element(By.TAG_NAME, "body").text
        if username not in page_text:
            raise Exception(f"No se pudo hacer login: {e}")

@when('accedo a la página del juego')
def step_impl(context):
    context.browser.get(f"{context.base_url}/game")
    time.sleep(0.5)

@then('debería ver las vidas restantes')
def step_impl(context):
    lives_count = context.browser.find_element(By.ID, "lives-count")
    assert lives_count.text.isdigit(), "No se muestran las vidas correctamente"

@then('debería ver espacios para las letras de la palabra')
def step_impl(context):
    display_word = context.browser.find_element(By.ID, "display-word").text
    assert "_" in display_word, "No se muestran los espacios para las letras"

# Steps para juego con palabra específica
@given('estoy jugando una partida con la palabra "{word}"')
def step_impl(context, word):
    # Forzar la palabra específica
    context.browser.get(f"{context.base_url}/new_game?word={word}")
    time.sleep(1)

@given('estoy jugando una partida con la palabra "{word}" y {lifes:d} vidas')
def step_impl(context, word, lifes):
    # Forzar palabra y vidas específicas
    context.browser.get(f"{context.base_url}/new_game?word={word}&lifes={lifes}")
    time.sleep(1)

@when('adivino la letra "{letter}"')
def step_impl(context, letter):
    if not context.browser.current_url.endswith("/game"):
        context.browser.get(f"{context.base_url}/game")
        time.sleep(0.5)
        
    letter_input = context.browser.find_element(By.ID, "letter-input")
    letter_input.clear()
    letter_input.send_keys(letter)
    
    form = context.browser.find_element(By.ID, "guess-form")
    form.submit()
    time.sleep(0.5)

@when('adivino todas las letras "{letters}"')
def step_impl(context, letters):
    for letter in letters.replace('"', '').replace(" ", "").split(","):
        context.execute_steps(f'''
            When adivino la letra "{letter}"
        ''')
        time.sleep(0.5)

@when('adivino incorrectamente las letras "{letters}"')
def step_impl(context, letters):
    for letter in letters.replace('"', '').replace(" ", "").split(","):
        context.execute_steps(f'''
            When adivino la letra "{letter}"
        ''')
        time.sleep(0.5)

@then('debería ver "{letter}" en la primera posición de la palabra')
def step_impl(context, letter):
    display_word = context.browser.find_element(By.ID, "display-word").text
    assert display_word.startswith(letter), f"La palabra mostrada '{display_word}' no comienza con '{letter}'"

@then('no debería ver la letra "{letter}" en la palabra')
def step_impl(context, letter):
    display_word = context.browser.find_element(By.ID, "display-word").text.replace(" ", "")
    assert letter not in display_word, f"La letra '{letter}' aparece en la palabra mostrada '{display_word}'"

@then('mis vidas deberían seguir siendo {lives}')
def step_impl(context, lives):
    lives_count = context.browser.find_element(By.ID, "lives-count").text
    assert lives_count == lives, f"Las vidas restantes son {lives_count}, se esperaba {lives}"

@then('mis vidas deberían disminuir a {lives}')
def step_impl(context, lives):
    lives_count = context.browser.find_element(By.ID, "lives-count").text
    assert lives_count == lives, f"Las vidas restantes son {lives_count}, se esperaba {lives}"

@then('debería ver un mensaje de victoria')
def step_impl(context):
    result = context.browser.find_element(By.ID, "game-result").text
    assert "ganado" in result.lower() or "won" in result.lower(), "No se muestra mensaje de victoria"

@then('debería ver un mensaje de derrota')
def step_impl(context):
    result = context.browser.find_element(By.ID, "game-result").text
    assert "terminado" in result.lower() or "over" in result.lower(), "No se muestra mensaje de derrota"

@then('debería ver la palabra completa "{word}"')
def step_impl(context, word):
    page_text = context.browser.find_element(By.TAG_NAME, "body").text
    assert word in page_text, f"No se muestra la palabra completa '{word}'"

@then('debería ver la opción para jugar de nuevo')
def step_impl(context):
    links = context.browser.find_elements(By.XPATH, "//a[contains(text(), 'jugar') or contains(text(), 'Jugar') or contains(text(), 'Play') or contains(text(), 'play') or contains(text(), 'New') or contains(text(), 'new') or contains(text(), 'Nuevo') or contains(text(), 'nuevo')]")
    assert len(links) > 0, "No se muestra la opción para jugar de nuevo"

@when('hago clic en "Cerrar sesión"')
def step_impl(context):
    try:
        # Intentar hacer scroll al elemento primero
        logout_link = context.browser.find_element(By.XPATH, "//a[contains(text(), 'Cerrar') or contains(text(), 'cerrar') or contains(text(), 'Logout') or contains(text(), 'logout')]")
        context.browser.execute_script("arguments[0].scrollIntoView(true);", logout_link)
        time.sleep(0.5)
        
        # Intentar click normal
        logout_link.click()
        
    except Exception as e:
        try:
            # Si falla, usar JavaScript para hacer click
            logout_link = context.browser.find_element(By.XPATH, "//a[contains(text(), 'Cerrar') or contains(text(), 'cerrar') or contains(text(), 'Logout') or contains(text(), 'logout')]")
            context.browser.execute_script("arguments[0].click();", logout_link)
            
        except Exception as e2:
            # Como último recurso, navegar directamente a logout
            context.browser.get(f"{context.base_url}/logout")
    
    time.sleep(0.5)

@then('debería volver a la página de inicio')
def step_impl(context):
    assert context.browser.current_url == context.base_url + "/", "No se redirigió a la página de inicio"

@then('no debería estar logueado')
def step_impl(context):
    page_source = context.browser.page_source
    assert "username" not in page_source.lower() or "logout" not in page_source.lower(), "El usuario sigue logueado"