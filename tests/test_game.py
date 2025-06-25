"""Unit tests for the HangmanGame class."""

from app.game import HangmanGame


def test_game_initial_state():
    """Test that the game displays the correct initial state."""
    game = HangmanGame("python")
    assert game.get_display_word() == "_ _ _ _ _ _"

def test_guess_correct_letter():
    """Test that guessing a correct letter reveals it in the word."""
    game = HangmanGame("python")
    game.guess("p")
    assert game.get_display_word() == "p _ _ _ _ _"

def test_guess_incorrect_letter():
    """Test that guessing an incorrect letter doesn't change the display."""
    game = HangmanGame("python")
    game.guess("a")
    assert game.get_display_word() == "_ _ _ _ _ _"

def test_remaining_lifes():
    """Test that remaining lives decrease with incorrect guesses."""
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
    """Test that guessing a letter reveals all occurrences in the word."""
    game = HangmanGame("letter")
    game.guess("t")
    assert game.get_display_word() == "_ _ t t _ _"
    game.guess("e")
    assert game.get_display_word() == "_ e t t e _"
    game.guess("r")
    assert game.get_display_word() == "_ e t t e r"

def test_game_over_no_lifes():
    """Test that the game ends when no lives remain."""
    game = HangmanGame("python", 2)
    game.guess("a")
    assert not game.is_game_over()
    game.guess("b")
    assert game.is_game_over()

def test_game_is_won():
    """Test that the game is won when all letters are guessed."""
    game = HangmanGame("python", 1)
    game.guess("p")
    game.guess("y")
    game.guess("t")
    game.guess("h")
    game.guess("o")
    game.guess("n")
    assert game.is_won()

def test_guess_word_correct():
    """Test that guessing the correct word wins the game."""
    game = HangmanGame("python", 3)
    result = game.guess_word("python")
    assert result is True
    assert game.is_won()
    assert game.get_display_word() == "p y t h o n"

def test_guess_word_incorrect():
    """Test that guessing an incorrect word loses a life."""
    game = HangmanGame("python", 3)
    initial_lives = game.get_remaining_lifes()
    result = game.guess_word("java")
    assert result is False
    assert not game.is_won()
    assert game.get_remaining_lifes() == initial_lives - 1

def test_guess_word_case_insensitive():
    """Test that word guessing is case insensitive."""
    game = HangmanGame("Python", 3)
    result = game.guess_word("PYTHON")
    assert result is True
    assert game.is_won()

def test_guess_word_game_over():
    """Test that incorrect word guess can end the game."""
    game = HangmanGame("python", 1)
    result = game.guess_word("wrong")
    assert result is False
    assert game.is_game_over()
    assert not game.is_won()

def test_repeated_letter_guess():
    """Test that guessing the same letter multiple times doesn't affect lives."""
    game = HangmanGame("python", 3)
    initial_lives = game.get_remaining_lifes()
    game.guess("a")  # incorrect letter
    game.guess("a")  # same incorrect letter again
    game.guess("a")  # same incorrect letter again
    assert game.get_remaining_lifes() == initial_lives - 1

def test_mixed_letter_and_word_guessing():
    """Test combining letter guesses with word guessing."""
    game = HangmanGame("cat", 3)
    game.guess("c")
    assert game.get_display_word() == "c _ _"
    result = game.guess_word("cat")
    assert result is True
    assert game.is_won()

def test_win_by_letters_only():
    """Test winning by guessing all letters without word guess."""
    game = HangmanGame("hi", 5)
    game.guess("h")
    assert not game.is_won()
    game.guess("i")
    assert game.is_won()
    assert game.get_display_word() == "h i"

def test_edge_case_single_letter_word():
    """Test game with single letter word."""
    game = HangmanGame("a", 2)
    assert game.get_display_word() == "_"
    game.guess("a")
    assert game.is_won()
    assert game.get_display_word() == "a"
