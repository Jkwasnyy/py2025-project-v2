from player import Player, CPUPlayer
from card import Deck
from hand_evaluator import HandEvaluator
from fileops.session_manager import SessionManager
from datetime import datetime
import uuid


class GameEngine:
    def __init__(self, players, deck, game_id=None):
        self.players = players
        self.deck = deck
        self.pot = 0
        self.current_bet = 0
        self.game_id = game_id or str(uuid.uuid4())
        self.session_mgr = SessionManager(data_dir="data")

    def collect_blinds(self, small_blind, big_blind):
        self.players[0].stack_amount -= small_blind
        self.players[1].stack_amount -= big_blind
        self.pot += small_blind + big_blind
        self.current_bet = big_blind
        print(f"Blindy: {self.players[0].get_name()} płaci {small_blind}, {self.players[1].get_name()} płaci {big_blind}")

    def betting_round(self):
        active_players = self.players.copy()
        for player in active_players:
            action = player.bet_prompt()

            if action == 'fold':
                print(f"{player.get_name()} pasuje.")
                self.players.remove(player)
                if len(self.players) == 1:
                    winner = self.players[0]
                    print(f"{winner.get_name()} wygrywa {self.pot}!")
                    winner.stack_amount += self.pot
                    self.pot = 0
                    self.save_session()
                    return

            elif action == 'call':
                bet_amount = min(self.current_bet, player.stack_amount)
                player.stack_amount -= bet_amount
                self.pot += bet_amount
                print(f"{player.get_name()} sprawdza {bet_amount}.")


            elif isinstance(action, tuple) and action[0] == "raise":
                raise_amount = action[1]
                self.current_bet += raise_amount
                player.stack_amount -= self.current_bet
                self.pot += self.current_bet
                print(f"{player.get_name()} podbija do {self.current_bet}.")

            elif action == 'raise':
                raise_amount = int(input(f"{player.get_name()} ile chcesz podbić? "))
                self.current_bet += raise_amount
                player.stack_amount -= self.current_bet
                self.pot += self.current_bet
                print(f"{player.get_name()} podbija do {self.current_bet}.")

    def showdown(self):
        if len(self.players) < 2:
            return  # Nie ma showdownu jeśli ktoś spasował

        p1, p2 = self.players
        hand1, hand2 = p1.get_player_hand(), p2.get_player_hand()
        rank1, _ = HandEvaluator.evaluate_hand(hand1)
        rank2, _ = HandEvaluator.evaluate_hand(hand2)
        name1 = HandEvaluator.get_hand_name(rank1)
        name2 = HandEvaluator.get_hand_name(rank2)

        print(f"{p1.get_name()} ma rękę {p1.cards_to_str()} ({name1})")
        print(f"{p2.get_name()} ma rękę {p2.cards_to_str()} ({name2})")

        result = HandEvaluator.compare_hands(hand1, hand2)
        if result == 1:
            p1.stack_amount += self.pot
            print(f"{p1.get_name()} wygrywa {self.pot}!")
        elif result == -1:
            p2.stack_amount += self.pot
            print(f"{p2.get_name()} wygrywa {self.pot}!")
        else:
            split = self.pot // 2
            p1.stack_amount += split
            p2.stack_amount += split
            print(f"Remis. Każdy gracz otrzymuje {split}")

        self.pot = 0
        self.save_session()

    def play_round(self, small_blind, big_blind):
        self.deck.shuffle()
        self.deck.deal(self.players)
        self.collect_blinds(small_blind, big_blind)

        for player in self.players:
            print(f"{player.get_name()} - {player.cards_to_str()}")
            idx = player.change_card_prompt()
            if idx is not None:
                new_card = self.deck.cards.pop()
                old_card = player.change_card(new_card, idx)
                print(f"{player.get_name()} wymienił {old_card} na {new_card}")

        self.betting_round()
        self.showdown()

    def build_session_data(self):
        return {
            "game_id": self.game_id,
            "timestamp": datetime.now().isoformat(),
            "players": [
                {
                    "id": i + 1,
                    "name": p.get_name(),
                    "stack": p.stack_amount,
                    "is_cpu": isinstance(p, CPUPlayer)
                }
                for i, p in enumerate(self.players)
            ],

            "pot": self.pot,
            "hands": {
                str(i + 1): [str(card) for card in p.get_player_hand()]
                for i, p in enumerate(self.players)
            }
        }


    def save_session(self):
        session = self.build_session_data()
        self.session_mgr.save_session(session)


if __name__ == "__main__":
    session_mgr = SessionManager()
    game_id = input("Podaj ID gry (lub Enter, aby rozpocząć nową): ").strip()

    if game_id:
        session = session_mgr.load_session(game_id)
        if session:
            print(f"Wczytano grę o ID {game_id}.")
            players = []
            for p in session["players"]:
                if p.get("is_cpu"):
                    players.append(CPUPlayer(p["stack"], p["name"]))
                else:
                    players.append(Player(p["stack"], p["name"]))
        else:
            print("Nie znaleziono sesji. Tworzymy nową grę.")
            players = [Player(1000, "Player1"), CPUPlayer(1000, "CPU")]
            game_id = str(uuid.uuid4())

            # Zapisz od razu nową sesję
            game = GameEngine(players, Deck(), game_id=game_id)
            game.save_session()
    else:
        players = [Player(1000, "Player1"), CPUPlayer(1000, "CPU")]
        game_id = str(uuid.uuid4())

        # Zapisz nową sesję
        game = GameEngine(players, Deck(), game_id=game_id)
        game.save_session()

    player1, player2 = players
    while player1.get_stack_amount() > 0 and player2.get_stack_amount() > 0:
        deck = Deck()
        game = GameEngine([player1, player2], deck, game_id=game_id)
        game.play_round(small_blind=25, big_blind=50)

        print(f"\nStan kont po rundzie:")
        print(f"{player1.get_name()}: {player1.get_stack_amount()}")
        print(f"{player2.get_name()}: {player2.get_stack_amount()}")

        cont = input("\nCzy chcesz kontynuować? (t/n): ").strip().lower()
        if cont != 't':
            print("\nGra zakończona przez gracza.")
            game.save_session()
            break

    print("\nGra zakończona!")
    if player1.get_stack_amount() <= 0:
        print(f"{player1.get_name()} zbankrutował.")
    if player2.get_stack_amount() <= 0:
        print(f"{player2.get_name()} zbankrutował.")
