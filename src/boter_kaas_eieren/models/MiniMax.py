from boter_kaas_eieren.game import Game


class MiniMax:
    game: Game
    
    def __init__(self, game):
        self.game = game

    def best_move(self):
        best_score = float("-inf")
        move = None
        for i in range(9):
            if self.game.board[i] == " ":
                self.game.board[i] = self.game.current_player
                score = self.minimax(0, False)
                self.game.board[i] = " "
                if score > best_score:
                    best_score = score
                    move = i
        return move

    def minimax(self, depth, is_maximizing):
        winner = self.game.winner()
        if winner == self.game.current_player:
            return 1
        elif winner and winner != self.game.current_player:
            return -1
        elif self.game.is_draw():
            return 0

        if is_maximizing:
            best_score = float("-inf")
            for i in range(9):
                if self.game.board[i] == " ":
                    self.game.board[i] = self.game.current_player
                    score = self.minimax(depth + 1, False)
                    self.game.board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(9):
                if self.game.board[i] == " ":
                    opponent = "O" if self.game.current_player == "X" else "X"
                    self.game.board[i] = opponent
                    score = self.minimax(depth + 1, True)
                    self.game.board[i] = " "
                    best_score = min(score, best_score)
            return best_score
