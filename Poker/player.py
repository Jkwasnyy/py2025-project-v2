import random

class Player:
    def __init__(self, money, name=""):
        self.__stack_ = money
        self.__name_ = name
        self.__hand_ = []

    @property
    def stack_amount(self):
        return self.__stack_

    @stack_amount.setter
    def stack_amount(self, amount):
        if amount < 0:
            raise ValueError("Gracz nie może mieć ujemnej ilości pieniędzy.")
        self.__stack_ = amount

    def take_card(self, card):
        self.__hand_.append(card)

    def get_stack_amount(self):
        return self.__stack_

    def change_card(self, card, idx):
        old_card = self.__hand_[idx]
        self.__hand_[idx] = card
        return old_card

    def get_player_hand(self):
        return self.__hand_

    def cards_to_str(self):
        return ', '.join(str(card) for card in self.__hand_)

    def get_name(self):
        return self.__name_

    def change_card_prompt(self):
        print(f"\n{self.__name_}, Twoje karty: {self.cards_to_str()}")
        while True:
            answer = input("Czy chcesz wymienić kartę? (tak/nie): ").strip().lower()
            if answer == "tak":
                print(f"Twoje karty: {self.cards_to_str()}")
                try:
                    card_index = int(input(f"Podaj numer karty do wymiany (1-{len(self.__hand_)}): ")) - 1
                    if 0 <= card_index < len(self.__hand_):
                        return card_index
                    else:
                        print("Nieprawidłowy numer karty. Spróbuj ponownie.")
                except ValueError:
                    print("Proszę podać numer karty.")
            elif answer == "nie":
                print("Nie wymieniasz żadnej karty.")
                return None
            else:
                print("Nie rozumiem odpowiedzi. Wpisz 'tak' lub 'nie'.")

    def bet_prompt(self):
        """Funkcja do zapytania o zakład gracza (fold, call, raise)."""
        while True:
            action = input(f"{self.__name_}, masz {self.__stack_} w stacku. Wybierz akcję: [call, raise, fold]: ").strip().lower()
            if action in ['call', 'raise', 'fold']:
                return action
            else:
                print("Niepoprawna akcja. Spróbuj ponownie.")

    def clear_hand(self):
        self.hand = []

class CPUPlayer(Player):
    def __init__(self, stack_amount, name="CPU"):
        super().__init__(stack_amount, name)

    def bet_prompt(self):
        action = random.choice(["fold", "call", "raise"])
        print(f"{self.get_name()} decyduje się na: {action}")

        if action == "raise":
            # Losowa kwota podbicia (np. 10–100)
            raise_amount = random.choice([10, 20, 50])
            print(f"{self.get_name()} podbija o {raise_amount}")
            return ("raise", raise_amount)
        return action

    def change_card_prompt(self):
        # 50% szans na wymianę jednej losowej karty
        if random.random() < 0.5:
            index = random.randint(0, 4)
            print(f"{self.get_name()} wymienia kartę nr {index + 1}")
            return index
        else:
            print(f"{self.get_name()} nie wymienia kart")
            return None

