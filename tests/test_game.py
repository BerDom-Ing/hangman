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
    assert game.get_remaining_lifes() == 5
    game.guess("a")
    assert game.get_remaining_lifes() == 4
    game.guess("b")
    assert game.get_remaining_lifes() == 3
    game.guess("c")
    assert game.get_remaining_lifes() == 2
    game.guess("d")
    assert game.get_remaining_lifes() == 1
    game.guess("e")
    assert game.get_remaining_lifes() == 0

def test_guess_word_with_two_same_letters():
    game = HangmanGame("letter")
    game.guess("t")
    assert game.get_display_word() == "_ _ t t _ _"
    game.guess("e")
    assert game.get_display_word() == "_ e t t e _"
    game.guess("r")
    assert game.get_display_word() == "_ e t t e r"

def test_game_over_no_lifes():
    game = HangmanGame("python", 2)
    game.guess("a")
    assert game.is_game_over() == False
    game.guess("b")
    assert game.is_game_over() == True

def test_game_is_won():
    game = HangmanGame("python", 1)
    game.guess("p")
    game.guess("y")
    game.guess("t")
    game.guess("h")
    game.guess("o")
    game.guess("n")
    assert game.is_won() == True