"""Flask web application for the Hangman game."""

import random

from flask import Flask, render_template, request, session, redirect, url_for
from app.game import HangmanGame

app = Flask(__name__)
app.secret_key = "hangman_secret_key"

# Lista de palabras para el juego
WORDS = ["python", "javascript", "hangman", "programming", "computer", "algorithm", "development"]


@app.route("/")
def index():
    """Render the main page or redirect to game if user is logged in."""
    # Si el usuario ya está logueado, redirige al juego
    if "username" in session:
        redirect(url_for("game_view"))
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    """Handle user login."""
    username = request.form.get("username", "").strip()
    # Verificar que username solo contiene caracteres alfanuméricos y tiene menos de 15 caracteres
    if username and username.isalnum() and len(username) < 15:
        session["username"] = username
        return redirect(url_for("new_game"))
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    """Handle user logout."""
    # Limpiar toda la sesión
    session.clear()
    return redirect(url_for("index"))


@app.route("/new_game")
def new_game():
    """Initialize a new game."""
    # Verificar si el usuario está logueado
    if "username" not in session:
        return redirect(url_for("index"))

    # Permitir configurar las vidas por query string
    try:
        lifes = int(request.args.get("lifes", 6))
    except ValueError:
        lifes = 6

    word = request.args.get("word")
    if not word:
        word = random.choice(WORDS)

    session["word"] = word
    session["initial_lifes"] = lifes
    session["current_lifes"] = lifes
    session["guessed_letters"] = []
    session["game_over"] = False
    session["won"] = False

    redirect(url_for("game_view"))


@app.route("/game")
def game_view():
    """Display the game page."""
    # Verificar si el usuario está logueado
    if "username" not in session:
        return redirect(url_for("index"))

    if "word" not in session:
        return redirect(url_for("new_game"))

    # Crear juego con vidas INICIALES
    hangman_game = HangmanGame(session["word"], session["initial_lifes"])

    # Restaurar el estado del juego
    hangman_game.guessed_letters = set(session["guessed_letters"])
    hangman_game.lifes = session["current_lifes"]

    game_over = session.get("game_over", hangman_game.is_game_over())
    won = session.get("won", hangman_game.is_won())

    return render_template(
        "game.html",
        username=session["username"],
        display_word=hangman_game.get_display_word(),
        lifes=hangman_game.get_remaining_lifes(),
        guessed_letters=sorted(hangman_game.guessed_letters),
        game_over=game_over,
        won=won
    )


@app.route("/guess", methods=["POST"])
def guess():
    """Handle letter guessing."""
    # Verificar si el usuario está logueado
    if "username" not in session:
        return redirect(url_for("index"))

    letter = request.form.get("letter", "").lower()

    if "word" not in session:
        return redirect(url_for("new_game"))

    if letter and len(letter) == 1 and letter.isalpha():
        if letter not in session["guessed_letters"]:
            # Crear juego con vidas INICIALES
            hangman_game = HangmanGame(session["word"], session["initial_lifes"])
            hangman_game.guessed_letters = set(session["guessed_letters"])
            hangman_game.lifes = session["current_lifes"]

            hangman_game.guess(letter)
            session["guessed_letters"] = list(hangman_game.guessed_letters)
            session["current_lifes"] = hangman_game.get_remaining_lifes()
            session["game_over"] = hangman_game.is_game_over()
            session["won"] = hangman_game.is_won()

    return redirect(url_for("game_view"))


if __name__ == "__main__":
    app.run(debug=True)
