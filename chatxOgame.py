#the code developed by chatGpt
##To upgrade your Tic-Tac-Toe game, we can enhance it by making the following changes:
#1.Improving the Logging Mechanism: Keep the latest score in a single file for easy access.
#2.Enhancing the UI: Center the result label for a better user experience.
#3.Reset Functionality: Ensure the result label and board reset properly.

import tkinter as tk
import random
import glob
import os

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.current_player = "X"
        self.player_score = 0
        self.computer_score = 0
        self.load_scores()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()
        
    def create_widgets(self):
        self.score_frame = tk.Frame(self.root)
        self.score_frame.grid(row=0, column=0, columnspan=3)
        
        self.player_label = tk.Label(self.score_frame, text=f"Player: {self.player_score}", font=('normal', 20))
        self.player_label.grid(row=0, column=0)
        
        self.computer_label = tk.Label(self.score_frame, text=f"Computer: {self.computer_score}", font=('normal', 20))
        self.computer_label.grid(row=0, column=1)
        
        self.restart_button = tk.Button(self.score_frame, text="Restart", command=self.reset_game, font=('normal', 20))
        self.restart_button.grid(row=0, column=2)
        
        self.result_label = tk.Label(self.root, text="", font=('normal', 30))
        self.result_label.grid(row=1, column=0, columnspan=3)
        
        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=2, column=0, columnspan=3)
        
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.button_frame, text="", font=('normal', 40, 'normal'), width=5, height=2,
                                   command=lambda r=row, c=col: self.on_button_click(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def on_button_click(self, row, col):
        if self.buttons[row][col]["text"] == "" and not self.check_winner():
            self.buttons[row][col]["text"] = self.current_player
            if self.check_winner():
                self.update_score()
                self.result_label.config(text=f"Player {self.current_player} wins!")
                self.log_result(f"Player {self.current_player} wins")
                self.root.after(2000, self.reset_board)  # Delay for 2 seconds before resetting the board
            elif self.is_tie():
                self.result_label.config(text="It's a tie!")
                self.log_result("It's a tie")
                self.root.after(2000, self.reset_board)  # Delay for 2 seconds before resetting the board
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.computer_move()

    def computer_move(self):
        if not self.check_winner() and not self.is_tie():
            empty_cells = [(r, c) for r in range(3) for c in range(3) if self.buttons[r][c]["text"] == ""]
            if empty_cells:
                row, col = random.choice(empty_cells)
                self.buttons[row][col]["text"] = self.current_player
                if self.check_winner():
                    self.result_label.config(text=f"Player {self.current_player} wins!")
                    self.log_result(f"Player {self.current_player} wins")
                    self.update_score()
                    self.root.after(2000, self.reset_board)  # Delay for 2 seconds before resetting the board
                elif self.is_tie():
                    self.result_label.config(text="It's a tie!")
                    self.log_result("It's a tie")
                    self.root.after(2000, self.reset_board)  # Delay for 2 seconds before resetting the board
                else:
                    self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        for row in range(3):
            if self.buttons[row][0]["text"] == self.buttons[row][1]["text"] == self.buttons[row][2]["text"] != "":
                return True
        for col in range(3):
            if self.buttons[0][col]["text"] == self.buttons[1][col]["text"] == self.buttons[2][col]["text"] != "":
                return True
        if self.buttons[0][0]["text"] == self.buttons[1][1]["text"] == self.buttons[2][2]["text"] != "":
            return True
        if self.buttons[0][2]["text"] == self.buttons[1][1]["text"] == self.buttons[2][0]["text"] != "":
            return True
        return False

    def is_tie(self):
        for row in range(3):
            for col in range(3):
                if self.buttons[row][col]["text"] == "":
                    return False
        return True

    def update_score(self):
        if self.current_player == "X":
            self.player_score += 1
            self.player_label.config(text=f"Player: {self.player_score}")
        else:
            self.computer_score += 1
            self.computer_label.config(text=f"Computer: {self.computer_score}")

    def enable_buttons(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]["state"] = "normal"

    def reset_board(self):
        self.current_player = "X"
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]["text"] = ""
        self.enable_buttons()
        self.result_label.config(text="")

    def reset_game(self):
        self.reset_board()
        self.player_score = 0
        self.computer_score = 0
        self.player_label.config(text=f"Player: {self.player_score}")
        self.computer_label.config(text=f"Computer: {self.computer_score}")
        self.clear_log()

    def load_scores(self):
        if os.path.exists("tictactoe_scores.txt"):
            with open("tictactoe_scores.txt", "r") as file:
                lines = file.readlines()
                self.player_score = int(lines[0].strip().split(": ")[1])
                self.computer_score = int(lines[1].strip().split(": ")[1])

    def log_result(self, result):
        with open("tictactoe_scores.txt", "w") as file:
            file.write(f"Player: {self.player_score}\n")
            file.write(f"Computer: {self.computer_score}\n")
            file.write(f"Result: {result}\n")

    def clear_log(self):
        if os.path.exists("tictactoe_scores.txt"):
            os.remove("tictactoe_scores.txt")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
