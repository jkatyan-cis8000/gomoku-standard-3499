"""Helper functions for Gomoku."""


def format_board(board: list[list[object]]) -> str:
    """Render the board as an ASCII string.
    
    Accepts board as list[list[None | 'B' | 'W']] and returns formatted output.
    """
    lines = []
    
    # Header with column numbers
    header = "   " + " ".join(f"{i:2d}" for i in range(len(board)))
    lines.append(header)
    
    # Board rows
    for row_idx, row in enumerate(board):
        row_str = f"{row_idx:2d} "
        for cell in row:
            if cell is None:
                row_str += " . "
            elif cell == "B":
                row_str += " B "
            elif cell == "W":
                row_str += " W "
            else:
                row_str += " . "
        lines.append(row_str)
    
    return "\n".join(lines)


def parse_position(input_str: str) -> tuple[int, int]:
    """Parse 'row,col' string to (row, col) tuple."""
    parts = input_str.strip().split(",")
    if len(parts) != 2:
        raise ValueError("Invalid position format. Use 'row,col' (e.g., '7,7')")
    row, col = int(parts[0]), int(parts[1])
    return (row, col)
