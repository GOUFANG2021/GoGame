import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import sys

# Ensure go_logic is in the Python path
sys.path.append('/mount/src/gogame/')

try:
    from go_logic import GoGame
except ModuleNotFoundError:
    st.error("Module 'go_logic' not found. Ensure it exists in the project directory.")

# Board settings
BOARD_SIZE = 19  # Go board 19x19
CELL_SIZE = 30
BOARD_PIXEL_SIZE = BOARD_SIZE * CELL_SIZE

def draw_board(board_state):
    """Draws the Go board with stones."""
    board = Image.new('RGB', (BOARD_PIXEL_SIZE, BOARD_PIXEL_SIZE), 'burlywood')
    draw = ImageDraw.Draw(board)
    
    # Draw grid
    for i in range(1, BOARD_SIZE):
        line_position = i * CELL_SIZE
        draw.line([(line_position, 0), (line_position, BOARD_PIXEL_SIZE)], fill='black', width=1)
        draw.line([(0, line_position), (BOARD_PIXEL_SIZE, line_position)], fill='black', width=1)
    
    # Draw stones
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board_state[x][y] == 1:
                draw.ellipse([(y * CELL_SIZE + 5, x * CELL_SIZE + 5), ((y + 1) * CELL_SIZE - 5, (x + 1) * CELL_SIZE - 5)], fill='black')
            elif board_state[x][y] == 2:
                draw.ellipse([(y * CELL_SIZE + 5, x * CELL_SIZE + 5), ((y + 1) * CELL_SIZE - 5, (x + 1) * CELL_SIZE - 5)], fill='white')
    
    return board

# Initialize GoGame instance with AI-enabled
try:
    game = GoGame(size=BOARD_SIZE)
except TypeError as e:
    st.error(f"Error initializing GoGame: {e}")

st.title("Go Game - Streamlit App")

if 'game_state' not in st.session_state:
    st.session_state.game_state = game.get_board()
    st.session_state.current_player = 1  # Start with Black

# Display the board
board_image = draw_board(st.session_state.game_state)
st.image(board_image, caption="Go Board", use_container_width=True)

# User move
col1, col2 = st.columns(2)
with col1:
    x = st.number_input("Enter row (0-18)", min_value=0, max_value=18, step=1, key="row")
with col2:
    y = st.number_input("Enter column (0-18)", min_value=0, max_value=18, step=1, key="col")

if st.button("Place Stone"):
    if game.place_stone(x, y):
        st.session_state.game_state = game.get_board()
        board_image = draw_board(st.session_state.game_state)
        st.image(board_image, caption="Go Board", use_container_width=True)

        # AI Move (Random for now, can be improved with an actual AI algorithm)
        empty_positions = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if game.board[i][j] == 0]
        if empty_positions:
            ai_x, ai_y = empty_positions[np.random.randint(len(empty_positions))]
            game.place_stone(ai_x, ai_y)
            st.session_state.game_state = game.get_board()
            board_image = draw_board(st.session_state.game_state)
            st.image(board_image, caption="Go Board (AI Played)", use_container_width=True)
