import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
from go_logic import GoGame

# Board settings
BOARD_SIZE = 19  # Go board 19x19
CELL_SIZE = 30
BOARD_PIXEL_SIZE = BOARD_SIZE * CELL_SIZE

game = GoGame(size=BOARD_SIZE, ai_enabled=True)

# Function to draw the board and stones
def draw_board():
    image = Image.new("RGB", (BOARD_PIXEL_SIZE, BOARD_PIXEL_SIZE), "#E3C16F")
    draw = ImageDraw.Draw(image)

    # Draw grid
    for i in range(BOARD_SIZE):
        offset = (i + 0.5) * CELL_SIZE
        draw.line([(offset, 0), (offset, BOARD_PIXEL_SIZE)], fill="black", width=1)
        draw.line([(0, offset), (BOARD_PIXEL_SIZE, offset)], fill="black", width=1)

    # Draw stones
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if game.board[i, j] != 0:
                color = "black" if game.board[i, j] == 1 else "white"
                x = (j + 0.5) * CELL_SIZE
                y = (i + 0.5) * CELL_SIZE
                draw.ellipse(
                    [(x - 10, y - 10), (x + 10, y + 10)], fill=color, outline="black"
                )
    return image

st.title("Go Game (19x19 Board)")
st.write("Click on the board to place your stone.")

if "game_state" not in st.session_state:
    st.session_state.game_state = game

# Display board
board_image = draw_board()
st.image(board_image, caption="Go Board", use_column_width=False)

# Capture mouse clicks
event = st.empty()
click = st.button("Click on board to play")

if click:
    coords = st.session_state.get("click_coords", None)
    if coords:
        x, y = coords
        if st.session_state.game_state.place_stone(y, x):  # Adjusted for row/column indexing
            st.experimental_rerun()
        else:
            st.warning("Invalid move! Try again.")

if st.button("Pass Turn"):
    if st.session_state.game_state.pass_turn():
        st.success("Game Over! Both players passed.")
    else:
        st.experimental_rerun()

# Display Updated Board
st.image(draw_board(), caption="Updated Go Board", use_column_width=False)

