from tkinter import *
from tkinter import messagebox
from game import Game
import time


class PazaakUI:
    def __init__(self) -> None:
        """Initialize the game UI, set up the window, widgets, and start the game."""
        self.game: Game = Game()
        self.window: Tk = Tk()
        self.window.title("Pazaak")
        self.window.config(padx=20, pady=20, background="black")
        self.canvas: Canvas = Canvas(width=1100, height=900)
        self.canvas.grid(row=0, column=0, columnspan=9, rowspan=6)
        self.score_label: Label = Label(text="X", fg="white", background="black")
        self.score_label.grid(column=0, row=0)
        self.score_label_opponent: Label = Label(text="X", fg="white", background="black")
        self.score_label_opponent.grid(column=5, row=0)
        self.dot_labels: list[Label] = []

        for i in range(1, 4):
            label = Label(text="X", fg="white", background="black")
            label.grid(column=i, row=0)
            self.dot_labels.append(label)
        self.dot_labels_opponent: list[Label] = []

        for i in range(6, 9):
            label = Label(text="X", fg="white", background="black")
            label.grid(column=i, row=0)
            self.dot_labels_opponent.append(label)
        self.card_labels: list[Label] = []

        for i in range(9):
            label = Label(text="X", fg="white", background="black")
            row = (i // 3) + 1
            column = i % 3
            label.grid(column=column, row=row)
            self.card_labels.append(label)
        self.card_labels_opponent: list[Label] = []

        for i in range(9):
            label = Label(text="X", fg="white", background="black")
            row = (i // 3) + 1
            column = (i % 3) + 5
            label.grid(column=column, row=row)
            self.card_labels_opponent.append(label)
        self.hand_card_buttons: list[Button] = []

        for i in range(4):
            button = Button(
                text="X",
                fg="white",
                background="black",
                command=lambda idx=i: self.ui_play_hand_card(idx),
            )
            button.grid(column=i, row=4)
            self.hand_card_buttons.append(button)
        self.opponent_hand_labels: list[Label] = []

        for i in range(4):
            label = Label(text="X", fg="white", background="black")
            label.grid(column=i + 5, row=4)
            self.opponent_hand_labels.append(label)

        for i in range(4):
            button = Button(
                text="invert",
                fg="white",
                background="black",
                command=lambda idx=i: self.ui_invert_card(idx),
            )
            button.grid(column=i, row=5)
        self.next_button: Button = Button(
            text="next", fg="white", background="black", command=self.process_turn
        )
        self.next_button.grid(column=4, row=4)
        self.pass_button: Button = Button(
            text="pass", fg="white", background="black", command=self.player_pass
        )
        self.pass_button.grid(column=4, row=5)

        self.show_rules()
        self.game.draw_hand()
        self.game.start()
        self.update_ui()
        self.window.mainloop()

    def update_hand_cards_ui(self) -> None:
        """Update the UI to reflect the current state of the player's and opponent's hand cards."""
        for i, button in enumerate(self.hand_card_buttons):
            if i < len(self.game.player_hand):
                button.config(text=self.game.player_hand[i])
            else:
                button.config(text="X")
        for i, label in enumerate(self.opponent_hand_labels):
            if i < len(self.game.opponent_hand):
                label.config(text=self.game.opponent_hand[i])
            else:
                label.config(text="X")

    def update_ui(self) -> None:
        """Update the entire UI, including boards, hand cards, and score labels."""
        self.update_board_ui()
        self.update_hand_card_ui()
        self.update_score_labels()

    def update_board_ui(self) -> None:
        """Update the UI to reflect the current state of the boards."""
        self.score_label.config(text=(sum(self.game.player_board)))
        for i, label in enumerate(self.card_labels):
            if i < len(self.game.player_board):
                label.config(text=self.game.player_board[i])
            else:
                label.config(text="X")
        self.score_label_opponent.config(text=(sum(self.game.opponent_board)))
        for i, label in enumerate(self.card_labels_opponent):
            if i < len(self.game.opponent_board):
                label.config(text=self.game.opponent_board[i])
            else:
                label.config(text="X")

    def update_hand_card_ui(self) -> None:
        """Update the UI for the player's and opponent's hand cards."""
        for i, button in enumerate(self.hand_card_buttons):
            if i < len(self.game.player_hand):
                button.config(text=self.game.player_hand[i])
            else:
                button.config(text="X")
        for i, label in enumerate(self.opponent_hand_labels):
            if i < len(self.game.opponent_hand):
                label.config(text=self.game.opponent_hand[i])
            else:
                label.config(text="X")

    def update_score_labels(self) -> None:
        """Update the score labels to show the number of rounds won by each player."""
        for i, label in enumerate(self.dot_labels):
            if i < self.game.player_rounds_won:
                label.config(text="O")
            else:
                label.config(text="X")
        for i, label in enumerate(self.dot_labels_opponent):
            if i < self.game.opponent_rounds_won:
                label.config(text="O")
            else:
                label.config(text="X")

    def ui_invert_card(self, index: int) -> None:
        """Invert the value of a hand card in the UI and update the UI."""
        self.game.invert_hand_card(index)
        self.update_hand_cards_ui()

    def disable_hand_cards(self) -> None:
        """Disable the player's hand card buttons."""
        for button in self.hand_card_buttons:
            button["state"] = "disabled"

    def enable_hand_cards(self) -> None:
        """Enable the player's hand card buttons."""
        for button in self.hand_card_buttons:
            button["state"] = "normal"

    def reset_round_ui(self) -> None:
        """Reset the UI and game state for a new round."""
        self.game.reset_round()
        self.update_ui()

    def ui_play_hand_card(self, index: int) -> None:
        """Handle the event of playing a hand card and update the UI."""
        card_played: bool = self.game.player_play_hand_card(index)
        if card_played:
            self.update_ui()
            self.disable_hand_cards()

    def disable_pass_button(self) -> None:
        """Disable the pass button."""
        self.pass_button["state"] = "disabled"

    def enable_pass_button(self) -> None:
        """Enable the pass button."""
        self.pass_button["state"] = "normal"

    def sleep(self) -> None:
        """Disable buttons, update UI, and wait for 1 second."""
        self.next_button["state"] = "disabled"
        if not self.game.player_passed:
            self.pass_button["state"] = "disabled"
        self.disable_hand_cards()
        self.window.update_idletasks()
        self.window.update()
        time.sleep(1)

    def end_sleep(self) -> None:
        """Re-enable buttons after sleep."""
        self.next_button["state"] = "normal"
        if not self.game.player_passed:
            self.pass_button["state"] = "normal"
        self.enable_hand_cards()

    def player_turn_ui(self) -> None:
        """Perform the player's turn in the UI and update the game state."""
        self.check_game_state()
        self.game.player_turn()
        self.update_ui()
        self.check_game_state()

    def opponent_turn_ui(self) -> None:
        """Perform the opponent's turn in the UI and update the game state."""
        self.game.opponent_turn()
        self.update_ui()
        self.check_game_state()

    def process_turn(self) -> None:
        """Handle the sequence of actions in a turn, including player and opponent moves."""
        if self.game.round_ended:
            self.game.round_ended = False
            return
        self.handle_exceeding_20()
        self.opponent_turn_ui()
        self.handle_exceeding_20()
        if self.game.round_ended:
            self.game.round_ended = False
            return
        self.sleep()
        self.end_sleep()
        self.enable_hand_cards()
        if not self.game.player_passed:
            self.player_turn_ui()
            if self.game.round_ended:
                self.game.round_ended = False
                return

    def check_game_state(self) -> None:
        """Check the current game state to determine if any immediate actions are required."""
        player_sum: int = sum(self.game.player_board)
        opponent_sum: int = sum(self.game.opponent_board)

        if player_sum == 20 and not self.game.player_passed:
            self.game.player_passed = True
            self.disable_pass_button()

        if opponent_sum == 20 and not self.game.opponent_passed:
            self.game.opponent_passed = True
            self.disable_pass_button()

        if self.game.player_passed and self.game.opponent_passed:
            self.evaluate_round_result()

    def handle_exceeding_20(self) -> None:
        """Handle the scenario where a player's total exceeds 20."""
        player_sum: int = sum(self.game.player_board)
        opponent_sum: int = sum(self.game.opponent_board)

        if player_sum > 20 and not self.game.player_passed:
            self.game.player_passed = True
            self.game.opponent_passed = True
            self.disable_pass_button()
            self.evaluate_round_result()
            return

        if opponent_sum > 20 and not self.game.opponent_passed:
            self.game.player_passed = True
            self.game.opponent_passed = True
            self.disable_pass_button()
            self.evaluate_round_result()

    def player_pass(self) -> None:
        """Handle the player passing their turn."""
        self.game.player_passed = True
        self.disable_pass_button()
        if self.game.player_passed and self.game.opponent_passed:
            if self.evaluate_round_result():
                self.reset_round_ui()

    def evaluate_round_result(self) -> bool:
        """Evaluate the result of a round and update the game state accordingly."""
        player_sum: int = sum(self.game.player_board)
        opponent_sum: int = sum(self.game.opponent_board)
        if self.game.player_passed and self.game.opponent_passed:
            if player_sum > 20:
                self.update_ui()
                self.game.opponent_rounds_won += 1
                messagebox.showinfo(title="End of Round", message="You lost the round.")
            elif opponent_sum > 20:
                self.update_ui()
                self.game.player_rounds_won += 1
                messagebox.showinfo(
                    title="End of Round",
                    message="You won the round.",
                )
            elif player_sum > opponent_sum:
                self.update_ui()
                self.game.player_rounds_won += 1
                messagebox.showinfo(title="End of Round", message="You won the round.")
            elif opponent_sum > player_sum:
                self.update_ui()
                self.game.opponent_rounds_won += 1
                messagebox.showinfo(title="End of Round", message="You lost the round.")
            else:
                self.update_ui()
                self.game.player_rounds_won += 1
                self.game.opponent_rounds_won += 1
                messagebox.showinfo(title="End of Round", message="It's a tie.")
            self.game.check_winner()
            self.reset_round_ui()
            self.enable_pass_button()
            self.game.round_ended = True
            return True
        return False

    def show_rules(self) -> None:
        """Display the game rules to the player."""
        ok: bool = messagebox.askokcancel(
            title="Game Rules", message="Would you like to learn the game rules?"
        )
        if ok:
            messagebox.showinfo(
                title="Game Rules",
                message=(
                    "Objective:\n"
                    "The goal of Pazaak is to have your total points on the board equal to or as close to 20 as possible without exceeding it.\n\n"
                    "Winning a Round:\n"
                    "- **Closest to 20**: If both players pass, the player with the total closest to 20 without exceeding it wins the round.\n"
                    "- **Exceeding 20 Points**: If a player exceeds 20 points and cannot reduce their total below or equal to 20 before ending their turn, they lose the round.\n\n"
                    "Winning the Game:\n"
                    "- The first player to win **three rounds** wins the game.\n\n"
                    "Gameplay:\n"
                    "- **Drawing Cards**: Each turn, a random card from the deck is automatically added to your board.\n"
                    "- **Hand Cards**: You have four hand cards per game, which you can play during your turn by clicking on them.\n"
                    "- **Inverting Cards**: Before playing a hand card, you can invert its value (e.g., change a +3 to a -3) by clicking the 'invert' button beneath it.\n"
                    "- **Next Turn**: Press 'next' to proceed to the next turn.\n"
                    "- **Passing**: Press 'pass' to end your turns for the current round; you cannot draw or play more cards after passing.\n"
                    "- **Automatic Pass at 20**: If your total points reach exactly 20, you automatically pass.\n"
                    "- **Over 20 Points**: If you exceed 20 points, you may still play hand cards to reduce your total back to 20 or below before ending your turn."
                ),
            )
