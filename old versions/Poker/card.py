import random

class Card:
    # Słownik symboli unicode
    unicode_dict = {'s': '\u2660', 'h': '\u2665', 'd': '\u2666', 'c': '\u2663'}

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def get_value(self):
        return (self.rank, self.suit)

    def __str__(self):
        return f'{self.rank}{Card.unicode_dict[self.suit]}'

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in ['s', 'h', 'd', 'c']
                      for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, players):
        for player in players:
            for _ in range(5):
                card = self.cards.pop()
                player.take_card(card)
