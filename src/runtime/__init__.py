"""Application orchestration and runtime wiring."""

from ..types import GameState, Player
from ..service import initialize_game, is_valid_move, apply_move, check_win, is_draw


class GameRunner:
    """Runs the game loop and manages state transitions."""
    
    def __init__(self, game: GameState | None = None):
        """Initialize with optional starting state."""
        self.game = game or initialize_game()
    
    def make_move(self, row: int, col: int) -> GameState:
        """Attempt a move and return the new state."""
        if not is_valid_move(self.game, row, col):
            raise ValueError("Invalid move")
        
        self.game = apply_move(self.game, row, col)
        return self.game
    
    def get_winner(self) -> str | None:
        """Get winner label or None if ongoing."""
        if self.game.winner is None:
            return None
        return self.game.winner.value
    
    def is_over(self) -> bool:
        """Check if game is over (win or draw)."""
        return self.game.winner is not None or is_draw(self.game)
    
    def save(self, file) -> None:
        """Save current game state to file."""
        from ..repo import save_game_state
        save_game_state(self.game, file)
    
    def load(self, file) -> None:
        """Load game state from file."""
        from ..repo import load_game_state
        self.game = load_game_state(file)
