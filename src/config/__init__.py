"""Configuration constants for the Gomoku game."""

from ..types import Player

# Board dimensions
BOARD_SIZE: int = 15

# Board markers
EMPTY: Player | None = None

# Players
BLACK: Player = Player.BLACK
WHITE: Player = Player.WHITE

# Win condition
WIN_LENGTH: int = 5

# Board initialization
EMPTY_BOARD: list[list[Player | None]] = [
    [EMPTY for _ in range(BOARD_SIZE)]
    for _ in range(BOARD_SIZE)
]
