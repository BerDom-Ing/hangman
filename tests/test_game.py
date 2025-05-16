from app.game import HangmanGame

def test_game_initial_state():
    game = HangmanGame("python")
    assert game.get_display_word() == "_ _ _ _ _ _"

def test_guess_correct_letter():
    game = HangmanGame("python")
    game.guess("p")
    assert game.get_display_word() == "p _ _ _ _ _"
