"""
ai_opponent.py
An AI opponent that predicts the player's next move and plays the counter
to it, instead of choosing randomly.

Two strategies are included:
  - FrequencyAI: predicts the player's overall most common move so far.
  - MarkovAI:    predicts the player's next move based on what they played
                 last time (a 1st-order Markov chain over Rock/Paper/Scissors).

AIOpponent starts with FrequencyAI (needs less data to be useful) and
switches to MarkovAI once enough rounds have been played, since Markov
chains pick up on patterns like "always switches after losing".
"""

import random
from collections import Counter, defaultdict

MOVES = ["Rock", "Paper", "Scissors"]

# BEATS[x] is the move that beats x.
BEATS = {"Rock": "Paper", "Paper": "Scissors", "Scissors": "Rock"}


def counter_move(move):
    """Return the move that beats the given move."""
    return BEATS[move]


def decide_winner(player_move, computer_move):
    """Returns 'Player', 'Computer', or 'Tie'."""
    if player_move == computer_move:
        return "Tie"
    if BEATS[player_move] == computer_move:
        return "Computer"
    return "Player"


class FrequencyAI:
    """Predicts the player's next move as whatever they've played most often."""

    def __init__(self, warmup_rounds=2):
        self.history = []
        self.warmup_rounds = warmup_rounds

    def record(self, player_move):
        self.history.append(player_move)

    def predict_player_move(self):
        if len(self.history) < self.warmup_rounds:
            return random.choice(MOVES)
        counts = Counter(self.history)
        return counts.most_common(1)[0][0]

    def choose_move(self):
        return counter_move(self.predict_player_move())


class MarkovAI:
    """
    Predicts the player's next move from their previous move, using a
    first-order Markov transition table:
        transitions[last_move][next_move] = count
    """

    def __init__(self, warmup_rounds=2):
        self.history = []
        self.transitions = defaultdict(lambda: {m: 0 for m in MOVES})
        self.warmup_rounds = warmup_rounds

    def record(self, player_move):
        if self.history:
            last = self.history[-1]
            self.transitions[last][player_move] += 1
        self.history.append(player_move)

    def predict_player_move(self):
        if len(self.history) < self.warmup_rounds:
            return random.choice(MOVES)

        last = self.history[-1]
        row = self.transitions[last]
        if sum(row.values()) == 0:
            counts = Counter(self.history)
            return counts.most_common(1)[0][0]
        return max(row, key=row.get)

    def choose_move(self):
        return counter_move(self.predict_player_move())


class AIOpponent:
    """
    Convenience wrapper: uses MarkovAI once enough history exists,
    otherwise falls back to FrequencyAI. Both models are fed every round
    so either can be swapped in seamlessly.
    """

    def __init__(self, warmup_rounds=3):
        self.frequency_ai = FrequencyAI(warmup_rounds=warmup_rounds)
        self.markov_ai = MarkovAI(warmup_rounds=warmup_rounds)
        self.warmup_rounds = warmup_rounds

    def record(self, player_move):
        self.frequency_ai.record(player_move)
        self.markov_ai.record(player_move)

    def choose_move(self):
        if len(self.markov_ai.history) >= self.warmup_rounds + 2:
            return self.markov_ai.choose_move()
        return self.frequency_ai.choose_move()

    def last_prediction(self):
        """What the AI currently 'thinks' the player will do (for on-screen display)."""
        if len(self.markov_ai.history) >= self.warmup_rounds + 2:
            return self.markov_ai.predict_player_move()
        return self.frequency_ai.predict_player_move()
