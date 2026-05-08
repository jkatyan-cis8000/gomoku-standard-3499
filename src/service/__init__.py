"""Core game logic for Gomoku.

Handles move validation, win detection, and game state transitions.
"""

from ..types import GameState, Player, Position, Move
from ..config import BOARD_SIZE, WIN_LENGTH, EMPTY_BOARD


def initialize_game() -> GameState:
    """Create an initial game state."""
    return GameState(
        board=EMPTY_BOARD,
        current_player=Player.BLACK,
        move_history=[],
        winner=None
    )


def is_valid_move(state: GameState, row: int, col: int) -> bool:
    """Check if a move at (row, col) is legal."""
    if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
        return False
    return state.board[row][col] is None


def apply_move(state: GameState, row: int, col: int) -> GameState:
    """Execute a move and return the new game state."""
    new_board = [list(r) for r in state.board]  # Deep copy
    new_board[row][col] = state.current_player
    
    new_history = state.move_history + [
        Move(player=state.current_player, position=Position(row=row, col=col))
    ]
    
    new_winner = check_win(new_board, row, col, state.current_player)
    
    next_player = Player.WHITE if state.current_player == Player.BLACK else Player.BLACK
    
    return GameState(
        board=new_board,
        current_player=next_player,
        move_history=new_history,
        winner=new_winner
    )


def check_win(board: list[list[Player | None]], row: int, col: int, player: Player) -> Player | None:
    """Check if the move at (row, col) wins the game."""
    if board[row][col] is None:
        return None
    
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal \
        (1, -1),  # diagonal /
    ]
    
    for dr, dc in directions:
        if _count_consecutive(board, row, col, dr, dc) + \
          _count_consecutive(board, row, col, -dr, -dc) - 1 >= WIN_LENGTH:
            return player
    
    return None


def _count_consecutive(board: list[list[Player | None]], row: int, col: int, dr: int, dc: int) -> int:
    """Count consecutive stones in one direction from (row, col)."""
    player = board[row][col]
    if player is None:
        return 0
    
    count = 0
    r, c = row, col
    while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
        count += 1
        r += dr
        c += dc
    
    return count


def is_draw(state: GameState) -> bool:
    """Check if the game is a draw (board full with no winner)."""
    if state.winner is not None:
        return False
    for row in state.board:
        for cell in row:
            if cell is None:
                return False
    return True
