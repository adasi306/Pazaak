import random
from tkinter import messagebox
import time


class Game:
    def __init__(self) -> None:
        """Initialize the game by setting up decks, hands, boards, and game state variables."""
        self.deck: list[int] = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]
        self.player_hand_deck: list[int] = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
        self.opponent_hand_deck: list[int] = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
        self.player_hand: list[int] = []
        self.opponent_hand: list[int] = []
        self.player_board: list[int] = []
        self.opponent_board: list[int] = []
        self.player_rounds_won: int = 0
        self.opponent_rounds_won: int = 0
        self.previous_player_rounds_won: int = 0
        self.previous_opponent_rounds_won: int = 0
        self.player_passed: bool = False
        self.opponent_passed: bool = False
        self.round_ended: bool = False

    def start(self) -> None:
        """Start the game by drawing the first card for the player's board."""
        card: int = self.draw_card()
        if card is not None:
            self.player_board.append(card)

    def draw_card(self) -> int:
        """Draw a random card from the main deck and return it."""
        try:
            card: int = random.choice(self.deck)
            self.deck.remove(card)
            return card
        except IndexError:
            return None

    def draw_hand(self) -> None:
        """Draw 4 random cards for both the player's and opponent's hands from their respective hand decks."""
        for _ in range(4):
            if self.player_hand_deck:
                card: int = random.choice(self.player_hand_deck)
                self.player_hand_deck.remove(card)
                self.player_hand.append(card)
        for _ in range(4):
            if self.opponent_hand_deck:
                card: int = random.choice(self.opponent_hand_deck)
                self.opponent_hand_deck.remove(card)
                self.opponent_hand.append(card)

    def player_play_hand_card(self, index: int) -> bool:
        """Play a hand card from the player's hand onto the player's board."""
        if 0 <= index < len(self.player_hand):
            card: int = self.player_hand.pop(index)
            self.player_board.append(card)
            return True
        return False

    def opponent_play_hand_card(
        self, to_reduce: bool = False, to_reach_17: bool = False, to_improve_score: bool = False
    ) -> bool:
        """Opponent plays a hand card based on specified strategy flags."""
        current_sum: int = sum(self.opponent_board)
        player_sum: int = sum(self.player_board)
        if to_reduce:
            for idx, card in enumerate(self.opponent_hand):
                inverted_card: int = -card
                new_sum: int = current_sum + inverted_card
                if new_sum <= 20:
                    self.opponent_hand.pop(idx)
                    self.opponent_board.append(inverted_card)
                    return True
            return False
        elif to_reach_17:
            for idx, card in enumerate(self.opponent_hand):
                new_sum: int = current_sum + card
                if 17 <= new_sum <= 20 and new_sum >= player_sum:
                    self.opponent_hand.pop(idx)
                    self.opponent_board.append(card)
                    return True
        elif to_improve_score:
            for idx, card in enumerate(self.opponent_hand):
                new_sum: int = current_sum + card
                if current_sum < new_sum <= 20 and new_sum >= player_sum:
                    self.opponent_hand.pop(idx)
                    self.opponent_board.append(card)
                    return True
        return False

    def invert_hand_card(self, index: int) -> None:
        """Invert the sign of a card in the player's hand."""
        if 0 <= index < len(self.player_hand):
            self.player_hand[index] *= -1

    def player_turn(self) -> None:
        """Perform player's turn by drawing a card if the player hasn't passed."""
        if not self.player_passed:
            card: int = self.draw_card()
            if card is not None:
                self.player_board.append(card)

    def opponent_turn(self) -> None:
        """Perform opponent's turn based on game logic and strategies."""
        if self.opponent_passed:
            return
        drawn_card: int = self.draw_card()
        if drawn_card is not None:
            self.opponent_board.append(drawn_card)
        opponent_sum: int = sum(self.opponent_board)
        player_sum: int = sum(self.player_board)
        if opponent_sum > 20:
            used_card: bool = self.opponent_play_hand_card(to_reduce=True)
            opponent_sum = sum(self.opponent_board)
            if used_card and 17 <= opponent_sum <= 20 and opponent_sum >= player_sum:
                time.sleep(1)
                self.opponent_passed = True
            return
        if self.player_passed and opponent_sum >= player_sum and opponent_sum <= 20:
            self.opponent_passed = True
            return
        if 17 <= opponent_sum <= 20:
            if opponent_sum >= player_sum:
                self.opponent_passed = True
                return
            else:
                used_card: bool = self.opponent_play_hand_card(to_improve_score=True)
                opponent_sum = sum(self.opponent_board)
                if used_card:
                    time.sleep(1)
                    if opponent_sum >= player_sum and opponent_sum <= 20:
                        self.opponent_passed = True
                    elif opponent_sum > 20:
                        used_card = self.opponent_play_hand_card(to_reduce=True)
                        opponent_sum = sum(self.opponent_board)
                        if opponent_sum <= 20 and opponent_sum >= player_sum:
                            self.opponent_passed = True
                        else:
                            self.opponent_passed = True
                    else:
                        self.opponent_passed = True
                else:
                    self.opponent_passed = True
                return
        if opponent_sum < 17:
            used_card: bool = self.opponent_play_hand_card(to_reach_17=True)
            opponent_sum = sum(self.opponent_board)
            if used_card and 17 <= opponent_sum <= 20 and opponent_sum >= player_sum:
                self.opponent_passed = True

    def check_winner(self) -> None:
        """Check if either player has won the game and reset if so."""
        if self.player_rounds_won == 3 and self.opponent_rounds_won == 3:
            self.player_rounds_won = 0
            self.opponent_rounds_won = 0
            messagebox.showinfo(title="Draw", message="The game ended in a draw.")
            self.reset_game()
        elif self.player_rounds_won == 3:
            self.player_rounds_won = 0
            self.opponent_rounds_won = 0
            messagebox.showinfo(title="Congratulations", message="You won the game.")
            self.reset_game()
        elif self.opponent_rounds_won == 3:
            self.player_rounds_won = 0
            self.opponent_rounds_won = 0
            messagebox.showinfo(title="Defeat", message="You lost the game.")
            self.reset_game()

    def reset_round(self) -> None:
        """Reset the game state for a new round."""
        self.round_ended = True
        self.deck = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]
        self.player_board.clear()
        self.opponent_board.clear()
        self.player_passed = False
        self.opponent_passed = False
        self.round_ended = False
        self.start()

    def reset_game(self) -> None:
        """Reset the entire game state for a new game."""
        self.reset_round()
        self.player_rounds_won = 0
        self.opponent_rounds_won = 0
        self.player_hand_deck = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
        self.opponent_hand_deck = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
        self.player_hand = []
        self.opponent_hand = []
        self.draw_hand()
