"""Core type definitions for the Gomoku game domain."""

from enum import Enum
from typing import NamedTuple


class Player(Enum):
    """Represents the two players in Gomoku."""
    BLACK = "B"
    WHITE = "W"


class Position(NamedTuple):
    """A position on the board."""
    row: int
    col: int


class Move(NamedTuple):
    """A player's move at a position."""
    player: Player
    position: Position


class GameState(NamedTuple):
    """Complete state of a Gomoku game."""
    board: list[list[Player | None]]  # 15x15 grid
    current_player: Player
    move_history: list[Move]
    winner: Player | None  # None if game ongoing
