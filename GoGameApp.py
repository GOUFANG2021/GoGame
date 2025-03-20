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

def draw_board():
    """Draws an empty Go board."""
    board = Image.new('RGB', (BOARD_PIXEL_SIZE, BOARD_PIXEL_SIZE), 'burlywood')
    draw = ImageDraw.Draw(board)
    for i in range(1, BOARD_SIZE):
        line_position = i * CELL_SIZE
        draw.line([(line_position, 0), (line_position, BOARD_PIXEL_SIZE)], fill='black', width=1)
        draw.line([(0, line_position), (BOARD_PIXEL_SIZE, line_position)], fill='black', width=1)
    return board

# Initialize GoGame instance with proper arguments
try:
    game = GoGame(size=BOARD_SIZE)
except TypeError as e:
    st.error(f"Error initializing GoGame: {e}")

st.title("Go Game - Streamlit App")

# Display the board
board_image = draw_board()
st.image(board_image, caption="Go Board", use_column_width=True)
