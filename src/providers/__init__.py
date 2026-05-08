"""Game state provider for dependency injection."""

from ..types import GameState, Player, Move


class GameStateProvider:
    """Provides game state instances."""
    
    def create_initial(self) -> GameState:
        """Create a fresh initial game state."""
        return GameState(
            board=[[None for _ in range(15)] for _ in range(15)],
            current_player=Player.BLACK,
            move_history=[],
            winner=None
        )
    
    def create_from_state(self, board: list[list[Player | None]], current_player: Player, history: list[Move], winner: Player | None = None) -> GameState:
        """Create a game state from components."""
        return GameState(board=board, current_player=current_player, move_history=history, winner=winner)
