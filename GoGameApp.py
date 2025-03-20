import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import copy
import random

# Improved GoGame Logic
class GoGame:
    def __init__(self, size=9):
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.current_player = 'B'  # Black starts

    def switch_player(self):
        self.current_player = 'W' if self.current_player == 'B' else 'B'

    def is_valid_move(self, x, y):
        if self.board[x][y] != '.':
            return False
        
        temp_board = copy.deepcopy(self)
        temp_board.board[x][y] = temp_board.current_player
        captured = temp_board.remove_captured_stones(x, y)
        
        if len(captured) == 0 and temp_board.count_liberties(x, y) == 0:
            return False
        return True
    
    def find_group(self, x, y):
        color = self.board[x][y]
        if color == '.':
            return []
        visited = set()
        queue = [(x, y)]
        group = []
        while queue:
            cx, cy = queue.pop(0)
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            group.append((cx, cy))
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.board[nx][ny] == color and (nx, ny) not in visited:
                        queue.append((nx, ny))
        return group
    
    def count_liberties(self, x, y):
        group = self.find_group(x, y)
        liberties = set()
        for (cx, cy) in group:
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.board[nx][ny] == '.':
                        liberties.add((nx, ny))
        return len(liberties)
    
    def remove_captured_stones(self, x, y):
        opponent = 'W' if self.current_player == 'B' else 'B'
        captured = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if self.board[nx][ny] == opponent:
                    group = self.find_group(nx, ny)
                    if self.count_liberties(nx, ny) == 0:
                        for (cx, cy) in group:
                            self.board[cx][cy] = '.'
                            captured.append((cx, cy))
        return captured
    
    def make_move(self, x, y):
        if not self.is_valid_move(x, y):
            return False
        
        self.board[x][y] = self.current_player
        self.remove_captured_stones(x, y)
        self.switch_player()
        return True
    
    def get_board(self):
        return self.board

# UI Implementation
st.title("Go Game - Streamlit App")
BOARD_SIZE = 9
CELL_SIZE = 40
BOARD_PIXEL_SIZE = BOARD_SIZE * CELL_SIZE

def draw_board(board_state):
    board = Image.new('RGB', (BOARD_PIXEL_SIZE, BOARD_PIXEL_SIZE), 'burlywood')
    draw = ImageDraw.Draw(board)
    
    for i in range(BOARD_SIZE):
        pos = i * CELL_SIZE + CELL_SIZE // 2
        draw.line([(pos, CELL_SIZE // 2), (pos, BOARD_PIXEL_SIZE - CELL_SIZE // 2)], fill='black', width=1)
        draw.line([(CELL_SIZE // 2, pos), (BOARD_PIXEL_SIZE - CELL_SIZE // 2, pos)], fill='black', width=1)
    
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board_state[x][y] == 'B':
                draw.ellipse([(y * CELL_SIZE + 5, x * CELL_SIZE + 5), (y * CELL_SIZE + CELL_SIZE - 5, x * CELL_SIZE + CELL_SIZE - 5)], fill='black')
            elif board_state[x][y] == 'W':
                draw.ellipse([(y * CELL_SIZE + 5, x * CELL_SIZE + 5), (y * CELL_SIZE + CELL_SIZE - 5, x * CELL_SIZE + CELL_SIZE - 5)], fill='white')
    
    return board

if 'game' not in st.session_state:
    st.session_state.game = GoGame(size=BOARD_SIZE)
    st.session_state.board_state = st.session_state.game.get_board()
    st.session_state.current_player = 'B'
    
st.image(draw_board(st.session_state.board_state), caption="Go Board")

col1, col2 = st.columns(2)
with col1:
    row = st.number_input("Row (1-9)", min_value=1, max_value=9, step=1) - 1
with col2:
    col = st.number_input("Column (A-I)", min_value=1, max_value=9, step=1) - 1

if st.button("Place Stone"):
    if st.session_state.game.make_move(row, col):
        st.session_state.board_state = st.session_state.game.get_board()
        st.experimental_rerun()
    else:
        st.warning("Invalid move!")

st.image(draw_board(st.session_state.board_state), caption="Updated Go Board")
