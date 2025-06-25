"""Hangman game logic module."""


class HangmanGame:
    """A class representing a Hangman game."""

    def __init__(self, word, lifes=6):
        """Initialize a new Hangman game.
        
        Args:
            word (str): The word to guess.
            lifes (int): Number of lives (default: 6).
        """
        self.lifes = lifes
        self.word = word.lower()
        self.guessed_letters = set()

    def guess(self, letter):
        """Guess a single letter.
        
        Args:
            letter (str): The letter to guess.
        """
        letter = letter.lower()
        if letter not in self.guessed_letters:
            self.guessed_letters.add(letter)
            if letter not in self.word:
                self.lifes -= 1

    def guess_word(self, word_guess):
        """Attempt to guess the entire word.
        
        Args:
            word_guess (str): The word to guess.
            
        Returns:
            bool: True if correct, False otherwise.
        """
        word_guess = word_guess.lower()
        if word_guess == self.word:
            # If correct, add all letters to guessed_letters to win the game
            for letter in self.word:
                self.guessed_letters.add(letter)
            return True
        # If incorrect, lose a life
        self.lifes -= 1
        return False

    def get_display_word(self):
        """Get the current display of the word with guessed letters revealed.
        
        Returns:
            str: The word with spaces and underscores.
        """
        return ' '.join([letter if letter in self.guessed_letters else "_" for letter in self.word])

    def is_game_over(self):
        """Check if the game is over (no lives remaining).
        
        Returns:
            bool: True if game is over, False otherwise.
        """
        return self.lifes <= 0

    def is_won(self):
        """Check if the game is won (all letters guessed).
        
        Returns:
            bool: True if game is won, False otherwise.
        """
        return all(letter in self.guessed_letters for letter in self.word)

    def get_remaining_lifes(self):
        """Get the number of remaining lives.
        
        Returns:
            int: Number of lives remaining.
        """
        return self.lifes
