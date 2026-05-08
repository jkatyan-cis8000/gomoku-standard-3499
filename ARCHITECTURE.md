# ARCHITECTURE.md

Written by team-lead before spawning teammates. This is the shared blueprint —
teammates read it to understand what they are building and how their module fits.

## Module Structure

- src/types.py: Core type definitions for the Gomoku game domain
- src/config.py: Board size, player symbols, and game constants
- src/repo/__init__.py: Game state persistence (in-memory and file-based)
- src/service/__init__.py: Core game logic (move validation, win detection)
- src/providers/__init__.py: Game state provider for dependency injection
- src/utils/__init__.py: Pure helper functions for display and parsing
- src/runtime/__init__.py: Application orchestration and wiring
- src/ui/__init__.py: CLI interface for user interaction

## Interfaces

### Types (`src/types.py`)
- `Player` (Enum): BLACK or WHITE
- `Position` (namedtuple): row, col for board coordinates
- `Move` (namedtuple): player, position for a game move
- `GameState` (namedtuple): board, current_player, move_history, winner

### Config (`src/config.py`)
- BOARD_SIZE: int = 15 (standard Gomoku board)
- EMPTY: any marker for empty cells
- BLACK: Player enum value
- WHITE: Player enum value
- WIN_LENGTH: int = 5 (stones needed to win)

### Service (`src/service/__init__.py`)
- `initialize_game() -> GameState`: Create initial game state
- `is_valid_move(state, row, col) -> bool`: Check if move is legal
- `apply_move(state, row, col) -> GameState`: Execute move, return new state
- `check_win(state, row, col) -> Player | None`: Check if this move wins
- `is_draw(state) -> bool`: Check for draw (board full with no winner)

### Providers (`src/providers/__init__.py`)
- `GameStateProvider`: Class to create and manage game states

### Utils (`src/utils/__init__.py`)
- `format_board(state) -> str`: Render board as ASCII
- `parse_position(input_str) -> Position`: Parse "row,col" string to Position

### UI (`src/ui/__init__.py`)
- `GameRunner`: Class that runs the game loop, handles input/output

## Shared Data Structures

```python
# Position
class Position(NamedTuple):
    row: int
    col: int

# Move
class Move(NamedTuple):
    player: Player
    position: Position

# GameState
class GameState(NamedTuple):
    board: list[list[Player | None]]  # 15x15 grid
    current_player: Player
    move_history: list[Move]
    winner: Player | None  # None if game ongoing

# Player
class Player(Enum):
    BLACK = "B"
    WHITE = "W"
```

## External Dependencies

None - this is a pure Python implementation with no external libraries.
