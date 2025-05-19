from app.game import HangmanGame

def test_game_initial_state():
    game = HangmanGame("python")
    assert game.get_display_word() == "_ _ _ _ _ _"

def test_guess_correct_letter():
    game = HangmanGame("python")
    game.guess("p")
    assert game.get_display_word() == "p _ _ _ _ _"

def test_guess_incorrect_letter():
    game = HangmanGame("python")
    game.guess("a")
    assert game.get_display_word() == "_ _ _ _ _ _"

def test_remaining_lifes():
    game = HangmanGame("python", 5)
    assert game.lifes == 5
    game.guess("a")
    assert game.lifes == 4
    game.guess("b")
    assert game.lifes == 3
    game.guess("c")
    assert game.lifes == 2
    game.guess("d")
    assert game.lifes == 1
    game.guess("e")
    assert game.lifes == 0