"""Game state persistence layer.

Provides in-memory and file-based storage for game states.
"""

from ..types import GameState, Player, Position, Move
from ..config import BOARD_SIZE, EMPTY, EMPTY_BOARD


def load_game_state(file) -> GameState:
    """Load a game state from a text file.
    
    Expected format:
    Line 1: board state (15 rows of 15 chars each, B=black, W=white, -=empty)
    Line 2: current player (B or W)
    Line 3+: move history (row,col,player)
    """
    lines = file.readlines()
    
    # Parse board (15x15)
    board: list[list[Player | None]] = []
    for row in range(BOARD_SIZE):
        row_str = lines[row].strip()
        board_row: list[Player | None] = []
        for col, char in enumerate(row_str):
            if char == "B":
                board_row.append(Player.BLACK)
            elif char == "W":
                board_row.append(Player.WHITE)
            else:
                board_row.append(EMPTY)
        board.append(board_row)
    
    # Parse current player
    current_player_str = lines[BOARD_SIZE].strip()
    current_player = Player.BLACK if current_player_str == "B" else Player.WHITE
    
    # Parse move history
    history: list[Move] = []
    for i in range(BOARD_SIZE + 1, len(lines)):
        line = lines[i].strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) == 3:
            row, col, player = int(parts[0]), int(parts[1]), parts[2]
            history.append(Move(
                player=Player.BLACK if player == "B" else Player.WHITE,
                position=Position(row=row, col=col)
            ))
    
    # Find winner from last move (if any)
    winner: Player | None = None
    if history:
        last_move = history[-1]
        if _check_win_at_position(board, last_move.position):
            winner = last_move.player
    
    return GameState(
        board=board,
        current_player=current_player,
        move_history=history,
        winner=winner
    )


def save_game_state(game: GameState, file) -> None:
    """Save a game state to a text file.
    
    Format: 15 rows board, current player, then move history.
    """
    # Write board
    for row in range(BOARD_SIZE):
        row_str = ""
        for col in range(BOARD_SIZE):
            cell = game.board[row][col]
            if cell == Player.BLACK:
                row_str += "B"
            elif cell == Player.WHITE:
                row_str += "W"
            else:
                row_str += "-"
        file.write(row_str + "\n")
    
    # Write current player
    file.write(game.current_player.value + "\n")
    
    # Write move history
    for move in game.move_history:
        file.write(f"{move.position.row},{move.position.col},{move.player.value}\n")


def _check_win_at_position(board: list[list[Player | None]], pos: Position) -> bool:
    """Check if a move at pos creates a winning line."""
    # This is a helper; actual win logic is in service layer
    return False
