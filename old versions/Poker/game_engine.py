from player import Player
from card import Deck
from hand_evaluator import HandEvaluator

class GameEngine:
    def __init__(self, players, deck):
        self.players = players
        self.deck = deck
        self.pot = 0
        self.current_bet = 0

    def collect_blinds(self, small_blind, big_blind):
        self.players[0].stack_amount -= small_blind
        self.players[1].stack_amount -= big_blind
        self.pot += small_blind + big_blind
        print(f"Blindy: {self.players[0].get_name()} płaci {small_blind}, {self.players[1].get_name()} płaci {big_blind}")

    def betting_round(self):
        for player in self.players:
            action = player.bet_prompt()

            if action == 'fold':
                print(f"{player.get_name()} pasuje.")
                self.players.remove(player)
                if len(self.players) == 1:
                    winner = self.players[0]
                    print(f"{winner.get_name()} wygrał {self.pot}!")
                    winner.stack_amount += self.pot
                    self.pot = 0
                    return
            elif action == 'call':
                if self.current_bet > player.stack_amount:
                    bet_amount = player.stack_amount
                    player.stack_amount = 0
                else:
                    bet_amount = self.current_bet
                    player.stack_amount -= bet_amount
                self.pot += bet_amount
                print(f"{player.get_name()} sprawdza {bet_amount}.")
            elif action == 'raise':
                raise_amount = int(input(f"{player.get_name()} ile chcesz podbić? "))
                self.current_bet += raise_amount
                player.stack_amount -= self.current_bet
                self.pot += self.current_bet
                print(f"{player.get_name()} podbija do {self.current_bet}.")

    def showdown(self):
        player1_name = self.players[0].get_name()
        player2_name = self.players[1].get_name()

        player1_hand = self.players[0].get_player_hand()
        player2_hand = self.players[1].get_player_hand()

        rank1, _ = HandEvaluator.evaluate_hand(player1_hand)
        rank2, _ = HandEvaluator.evaluate_hand(player2_hand)
        name1 = HandEvaluator.get_hand_name(rank1)
        name2 = HandEvaluator.get_hand_name(rank2)

        print(f"{player1_name} ma rękę {self.players[0].cards_to_str()} ({name1})")
        print(f"{player2_name} ma rękę {self.players[1].cards_to_str()} ({name2})")

        result = HandEvaluator.compare_hands(player1_hand, player2_hand)

        if result == 1:
            winner = self.players[0]
            print(f"{winner.get_name()} wygrał {self.pot}!")
            winner.stack_amount += self.pot
        elif result == -1:
            winner = self.players[1]
            print(f"{winner.get_name()} wygrał {self.pot}!")
            winner.stack_amount += self.pot
        else:
            print(f"Remis! Obaj gracze mieli: {name1}. Pula jest dzielona.")
            self.players[0].stack_amount += self.pot // 2
            self.players[1].stack_amount += self.pot // 2

        self.pot = 0

    def play_round(self, small_blind, big_blind):
        self.collect_blinds(small_blind, big_blind)
        self.deck.shuffle()
        self.deck.deal(self.players)

        for player in self.players:
            print(f"{player.get_name()} - {player.cards_to_str()}")

        for player in self.players:
            change_card_index = player.change_card_prompt()
            if change_card_index is not None:
                new_card = self.deck.cards.pop()
                old_card = player.change_card(new_card, change_card_index)
                print(f"{player.get_name()} wymienił kartę {old_card} na {new_card}")

        self.betting_round()
        self.showdown()

if __name__ == "__main__":
    player1 = Player(1000, "Player1")
    player2 = Player(1000, "Player2")
    deck = Deck()
    game = GameEngine([player1, player2], deck)
    game.play_round(small_blind=25, big_blind=50)
