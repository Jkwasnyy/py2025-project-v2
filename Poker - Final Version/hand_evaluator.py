from collections import Counter

RANK_ORDER = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
              '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}


class HandEvaluator:
    HAND_RANKS = {
        "high_card": 1,
        "one_pair": 2,
        "two_pair": 3,
        "three_of_a_kind": 4,
        "straight": 5,
        "flush": 6,
        "full_house": 7,
        "four_of_a_kind": 8,
        "straight_flush": 9
    }

    RANK_NAMES = {v: k.replace('_', ' ').title() for k, v in HAND_RANKS.items()}

    @staticmethod
    def evaluate_hand(hand):
        ranks = sorted([RANK_ORDER[card.rank] for card in hand], reverse=True)
        suits = [card.suit for card in hand]

        rank_counter = Counter(ranks)
        rank_counts = sorted(rank_counter.items(), key=lambda x: (-x[1], -x[0]))
        counts = [cnt for val, cnt in rank_counts]
        values = [val for val, cnt in rank_counts]

        is_flush = len(set(suits)) == 1
        is_straight = all([ranks[i] - 1 == ranks[i + 1] for i in range(4)])

        if ranks == [14, 5, 4, 3, 2]:  # Special low-Ace straight
            is_straight = True
            ranks = [5, 4, 3, 2, 1]

        if is_straight and is_flush:
            return (HandEvaluator.HAND_RANKS["straight_flush"], ranks)
        elif counts[0] == 4:
            return (HandEvaluator.HAND_RANKS["four_of_a_kind"], values)
        elif counts[0] == 3 and counts[1] == 2:
            return (HandEvaluator.HAND_RANKS["full_house"], values)
        elif is_flush:
            return (HandEvaluator.HAND_RANKS["flush"], ranks)
        elif is_straight:
            return (HandEvaluator.HAND_RANKS["straight"], ranks)
        elif counts[0] == 3:
            return (HandEvaluator.HAND_RANKS["three_of_a_kind"], values)
        elif counts[0] == 2 and counts[1] == 2:
            return (HandEvaluator.HAND_RANKS["two_pair"], values)
        elif counts[0] == 2:
            return (HandEvaluator.HAND_RANKS["one_pair"], values)
        else:
            return (HandEvaluator.HAND_RANKS["high_card"], ranks)

    @staticmethod
    def get_hand_name(rank_value):
        return HandEvaluator.RANK_NAMES.get(rank_value, "Unknown")

    @staticmethod
    def compare_hands(hand1, hand2):
        rank1, tiebreakers1 = HandEvaluator.evaluate_hand(hand1)
        rank2, tiebreakers2 = HandEvaluator.evaluate_hand(hand2)

        if rank1 != rank2:
            return 1 if rank1 > rank2 else -1

        for a, b in zip(tiebreakers1, tiebreakers2):
            if a != b:
                return 1 if a > b else -1

        return 0  # Tie
