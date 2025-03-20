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
try:
    game = GoGame(size=BOARD_SIZE)
except TypeError as e:
    st.error(f"Error initializing GoGame: {e}")

st.title("Go Game - Streamlit App")

if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'game_state' not in st.session_state:
    st.session_state.game_state = game.get_board()
    st.session_state.current_player = 1  # Start with Black

# Buttons to Start and Finish Game
col1, col2 = st.columns(2)
with col1:
    if st.button("Start Game"):
        st.session_state.game_started = True
        game = GoGame(size=BOARD_SIZE)
        st.session_state.game_state = game.get_board()
        st.session_state.current_player = 1
        st.experimental_rerun()

with col2:
    if st.button("Finish Game"):
        st.session_state.game_started = False
        st.write("Game Over! Thank you for playing.")
        st.stop()

if st.session_state.game_started:
    # Display the board and handle user clicks
    board_image = draw_board(st.session_state.game_state)
    st.image(board_image, caption="Go Board", use_container_width=True)
    
    # Capture user click input
    click_location = st.image(board_image, caption="Click on the board to place a stone", use_container_width=True)
    
    if 'last_click' in st.session_state:
        x, y = st.session_state.last_click
        if game.place_stone(x, y):
            st.session_state.game_state = game.get_board()
            board_image = draw_board(st.session_state.game_state)
            st.image(board_image, caption="Go Board", use_container_width=True)
            
            # AI Move (Random move for now, can be replaced with a real AI algorithm)
            empty_positions = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if game.board[i][j] == 0]
            if empty_positions:
                ai_x, ai_y = empty_positions[np.random.randint(len(empty_positions))]
                game.place_stone(ai_x, ai_y)
                st.session_state.game_state = game.get_board()
                st.image(draw_board(st.session_state.game_state), caption="Go Board (AI Played)", use_container_width=True)
