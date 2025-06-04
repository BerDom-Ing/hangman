from flask import Flask, render_template, request, session, redirect, url_for
from app.game import HangmanGame
import random

app = Flask(__name__)
app.secret_key = "hangman_secret_key"

# Lista de palabras para el juego
WORDS = ["python", "javascript", "hangman", "programming", "computer", "algorithm", "development"]

@app.route("/")
def index():
    # Si el usuario ya está logueado, redirige al juego
    if "username" in session:
        return redirect(url_for("game"))
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    # Verificar que username solo contiene caracteres alfanuméricos y tiene menos de 15 caracteres
    if username and username.isalnum() and len(username) < 15:
        session["username"] = username
        return redirect(url_for("new_game"))
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    # Limpiar toda la sesión
    session.clear()
    return redirect(url_for("index"))

@app.route("/new_game")
def new_game():
    # Verificar si el usuario está logueado
    if "username" not in session:
        return redirect(url_for("index"))
    
    # Permitir configurar las vidas por query string
    try:
        lifes = int(request.args.get("lifes", 6))
    except ValueError:
        lifes = 6

    word = random.choice(WORDS)
    session["word"] = word
    session["initial_lifes"] = lifes  
    session["current_lifes"] = lifes  
    session["guessed_letters"] = []
    return redirect(url_for("game"))

@app.route("/game")
def game():
    # Verificar si el usuario está logueado
    if "username" not in session:
        return redirect(url_for("index"))
        
    if "word" not in session:
        return redirect(url_for("new_game"))
    
    # Crear juego con vidas INICIALES
    game = HangmanGame(session["word"], session["initial_lifes"])
    
    # Restaurar el estado del juego
    game.guessed_letters = set(session["guessed_letters"])
    game.lifes = session["current_lifes"]  
    
    return render_template(
        "game.html", 
        username=session["username"],
        display_word=game.get_display_word(),
        lifes=game.get_remaining_lifes(),
        guessed_letters=sorted(game.guessed_letters),
        game_over=game.is_game_over(),
        won=game.is_won()
    )

@app.route("/guess", methods=["POST"])
def guess():
    # Verificar si el usuario está logueado
    if "username" not in session:
        return redirect(url_for("index"))
        
    letter = request.form.get("letter", "").lower()
    
    if "word" not in session:
        return redirect(url_for("new_game"))
    
    if letter and len(letter) == 1 and letter.isalpha():
        if letter not in session["guessed_letters"]:
            # Crear juego con vidas INICIALES
            game = HangmanGame(session["word"], session["initial_lifes"])
            game.guessed_letters = set(session["guessed_letters"])
            game.lifes = session["current_lifes"]  # ← CAMBIAR: restaurar vidas actuales
            
            game.guess(letter)
            session["guessed_letters"] = list(game.guessed_letters)
            session["current_lifes"] = game.get_remaining_lifes()  # ← CAMBIAR: guardar vidas actuales
    
    return redirect(url_for("game"))

if __name__ == "__main__":
    app.run(debug=True)