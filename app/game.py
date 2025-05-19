class HangmanGame:
    def __init__(self, word, lifes=6):
        self.lifes = lifes
        self.word = word.lower()
        self.guessed_letters = set()

    def guess(self, letter):
        letter = letter.lower()
        self.guessed_letters.add(letter)
        if letter not in self.word:
            self.lifes -= 1

    def get_display_word(self):
        return ' '.join([letter if letter in self.guessed_letters else "_" for letter in self.word])

