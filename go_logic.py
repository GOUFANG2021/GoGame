import numpy as np

class GoGame:
    def __init__(self, size=19):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)  # 0 = empty, 1 = black, 2 = white
        self.current_player = 1  # Black starts first
        self.previous_board = None  # Used for Ko rule
        self.pass_count = 0  # Track consecutive passes

    def switch_player(self):
        """Switch turn between players"""
        self.current_player = 3 - self.current_player  # Toggle between 1 (Black) and 2 (White)

    def is_valid_move(self, x, y):
        """Check if move is valid"""
        if self.board[x, y] != 0:
            return False  # Position already occupied
        return True

    def place_stone(self, x, y):
        """Attempt to place a stone on the board"""
        if not self.is_valid_move(x, y):
            return False
        
        # Save board state for Ko rule
        self.previous_board = self.board.copy()
        self.board[x, y] = self.current_player
        
        # Capture opponent stones if applicable
        self.capture_stones()
        
        # Prevent Ko rule violation
        if np.array_equal(self.board, self.previous_board):
            self.board[x, y] = 0  # Undo the move
            return False
        
        self.switch_player()
        self.pass_count = 0  # Reset pass counter when a move is made
        return True

    def capture_stones(self):
        """Check for captured stones and remove them"""
        opponent = 3 - self.current_player
        visited = set()
        to_remove = set()
        
        def dfs(i, j, group):
            """Depth-first search to find connected stones"""
            if (i, j) in visited:
                return
            if not (0 <= i < self.size and 0 <= j < self.size):
                return
            if self.board[i, j] == 0:
                group.clear()
                return
            if self.board[i, j] == self.current_player:
                return
            
            visited.add((i, j))
            group.add((i, j))
            
            # Check all 4 directions
            dfs(i-1, j, group)
            dfs(i+1, j, group)
            dfs(i, j-1, group)
            dfs(i, j+1, group)
        
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i, j] == opponent and (i, j) not in visited:
                    group = set()
                    dfs(i, j, group)
                    if group:  # If surrounded, remove stones
                        to_remove.update(group)
        
        for (i, j) in to_remove:
            self.board[i, j] = 0

    def pass_turn(self):
        """Handle a player passing their turn"""
        self.pass_count += 1
        self.switch_player()
        if self.pass_count >= 2:  # Two consecutive passes end the game
            return True  # Game Over
        return False

    def get_board(self):
        """Return the current state of the board"""
        return self.board

    def is_game_over(self):
        """Check if the game is over (two consecutive passes)"""
        return self.pass_count >= 2

# Example Usage:
if __name__ == "__main__":
    game = GoGame(size=9)  # Initialize a 9x9 board
    game.place_stone(4, 4)  # Black moves
    game.place_stone(4, 5)  # White moves
    print(game.get_board())

