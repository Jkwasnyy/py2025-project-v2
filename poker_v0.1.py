import random


class Card:
    # słownik symboli unicode
    unicode_dict = {'s': '\u2660', 'h': '\u2665', 'd': '\u2666', 'c': '\u2663'}

    def __init__(self, rank, suit):
        # TODO: definicja konstruktora, ma ustawiać pola rangi i koloru.
        self.rank = rank
        self.suit = suit

    def get_value(self):
        # TODO: definicja metody (ma zwracać kartę w takiej reprezentacji, jak dotychczas, tzn. krotka)
        return (self.rank, self.suit)

    def __str__(self):
        # TODO: definicja metody, przydatne do wypisywania karty
        return f'{self.rank}{Card.unicode_dict[self.suit]}'


class Deck():
    def __init__(self, *args):
        # TODO: definicja metody, ma tworzyć niepotasowaną talię (jak na poprzednich lab)
        self.cards = [Card(rank, suit) for suit in ['s','h','d','c'] for rank in ['2','3','4','5','6','7','8','9','10','J','Q','K','A']]

    def __str__(self):
        # TODO: definicja metody, przydatne do wypisywania karty
        return ', '.join(str(card) for card in self.cards)

    def shuffle(self):
        # TODO: definicja metody, tasowanie
        random.shuffle(self.cards)

    def deal(self, players):
        # TODO: definicja metody, otrzymuje listę graczy i rozdaje im karty wywołując na nich metodę take_card z Player
        for player in players:
            for _ in range(5):
                card = self.cards.pop()
                player.take_card(card)


class Player():

    def __init__(self, money, name=""):
        self.__stack_ = money
        self.__name_ = name
        self.__hand_ = []

    def take_card(self, card):
        self.__hand_.append(card)

    def get_stack_amount(self):
        return self.__stack_

    def change_card(self, card, idx):
        # TODO: przyjmuje nową kartę, wstawia ją za kartę o indeksie idx, zwraca kartę wymienioną
        old_card = self.__hand_[idx]
        self.__hand_[idx] = card
        return old_card

    def get_player_hand(self):
        return tuple(self.__hand_)

    def cards_to_str(self):
        # TODO: definicja metody, zwraca stringa z kartami gracza
        return ', '.join(str(card) for card in self.__hand_)

    # TODO: OPCJONALNE Pozyskanie nazwy gracza
    def get_name(self):
        return self.__name_

player1 = Player(100, "Player1")
player2 = Player(150, "Player2")

deck = Deck()
deck.shuffle()

deck.deal([player1, player2])

print(f'{player1.get_name()} - {player1.cards_to_str()} - {player1.get_stack_amount()} Tokens ')
print(f'{player2.get_name()} - {player2.cards_to_str()} - {player2.get_stack_amount()} Tokens ')
