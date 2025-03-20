import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import sys

# GoGame Logic Implementation
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
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x, y] == 0

    def place_stone(self, x, y):
        """Attempt to place a stone on the board"""
        if not self.is_valid_move(x, y):
            return False
        
        self.previous_board = self.board.copy()
        self.board[x, y] = self.current_player
        
        self.switch_player()
        self.pass_count = 0
        return True

    def get_board(self):
        """Return the current state of the board"""
        return self.board.tolist()

# Board settings
BOARD_SIZE = 19  # Go board 19x19
CELL_SIZE = 30
BOARD_PIXEL_SIZE = BOARD_SIZE * CELL_SIZE

def draw_board(board_state):
    """Draws the Go board with stones."""
    board = Image.new('RGB', (BOARD_PIXEL_SIZE, BOARD_PIXEL_SIZE), 'burlywood')
    draw = ImageDraw.Draw(board)
    
    # Draw grid
    for i in range(BOARD_SIZE):
        line_position = i * CELL_SIZE + CELL_SIZE // 2
        draw.line([(line_position, CELL_SIZE // 2), (line_position, BOARD_PIXEL_SIZE - CELL_SIZE // 2)], fill='black', width=1)
        draw.line([(CELL_SIZE // 2, line_position), (BOARD_PIXEL_SIZE - CELL_SIZE // 2, line_position)], fill='black', width=1)
    
    # Draw stones at the line intersections
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board_state[x][y] == 1:
                draw.ellipse([(y * CELL_SIZE + CELL_SIZE // 2 - 10, x * CELL_SIZE + CELL_SIZE // 2 - 10), 
                              (y * CELL_SIZE + CELL_SIZE // 2 + 10, x * CELL_SIZE + CELL_SIZE // 2 + 10)], fill='black')
            elif board_state[x][y] == 2:
                draw.ellipse([(y * CELL_SIZE + CELL_SIZE // 2 - 10, x * CELL_SIZE + CELL_SIZE // 2 - 10), 
                              (y * CELL_SIZE + CELL_SIZE // 2 + 10, x * CELL_SIZE + CELL_SIZE // 2 + 10)], fill='white')
    
    return board

# Initialize GoGame instance
game = GoGame(size=BOARD_SIZE)

st.title("Go Game - Streamlit App")

if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'game_state' not in st.session_state:
    st.session_state.game_state = game.get_board()
if 'player_color' not in st.session_state:
    st.session_state.player_color = 1  # Default to black

# Choose player color
if not st.session_state.game_started:
    st.session_state.player_color = st.radio("Choose your color:", [1, 2], format_func=lambda x: "Black" if x == 1 else "White")

# Buttons to Start and Finish Game
col1, col2 = st.columns(2)
with col1:
    if st.button("Start Game"):
        st.session_state.game_started = True
        game = GoGame(size=BOARD_SIZE)
        st.session_state.game_state = game.get_board()
        if st.session_state.player_color == 2:
            empty_positions = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if game.board[i][j] == 0]
            if empty_positions:
                ai_x, ai_y = empty_positions[np.random.randint(len(empty_positions))]
                game.place_stone(ai_x, ai_y)
                st.session_state.game_state = game.get_board()
        st.rerun()

with col2:
    if st.button("Finish Game"):
        st.session_state.game_started = False
        st.write("Game Over! Thank you for playing.")
        st.stop()

if st.session_state.game_started:
    # Display the board and handle user clicks
    board_image = draw_board(st.session_state.game_state)
    st.image(board_image, caption="Go Board", use_container_width=True)
    
    click_x = st.slider("Select X Coordinate (0-18)", 0, 18, 9)
    click_y = st.slider("Select Y Coordinate (0-18)", 0, 18, 9)
    
    if st.button("Place Stone"):
        if game.place_stone(click_x, click_y):
            st.session_state.game_state = game.get_board()
            
            # AI Move (Random move for now, can be replaced with a real AI algorithm)
            empty_positions = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if game.board[i][j] == 0]
            if empty_positions:
                ai_x, ai_y = empty_positions[np.random.randint(len(empty_positions))]
                game.place_stone(ai_x, ai_y)
                st.session_state.game_state = game.get_board()
                
            st.rerun()
