class HangmanGame:
    def __init__(self, word):
        self.word = word.lower()
        self.guessed_letters = set()

    def guess(self, letter):
        self.guessed_letters.add(letter.lower())

    def get_display_word(self):
        return ' '.join([letter if letter in self.guessed_letters else "_" for letter in self.word])
