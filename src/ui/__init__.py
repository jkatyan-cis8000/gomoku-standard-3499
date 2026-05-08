"""CLI interface for Gomoku."""

from ..runtime import GameRunner


def format_board_simple(board: list[list[object]]) -> str:
    """Simple board formatter for CLI."""
    lines = []
    header = "   " + " ".join(f"{i:2d}" for i in range(len(board)))
    lines.append(header)
    
    for row_idx, row in enumerate(board):
        row_str = f"{row_idx:2d} "
        for cell in row:
            if cell is None:
                row_str += " . "
            elif hasattr(cell, 'value') and cell.value == "B":
                row_str += " B "
            elif hasattr(cell, 'value') and cell.value == "W":
                row_str += " W "
            elif cell == "B":
                row_str += " B "
            elif cell == "W":
                row_str += " W "
            else:
                row_str += " . "
        lines.append(row_str)
    
    return "\n".join(lines)


def parse_move(cmd: str) -> tuple[int, int]:
    """Parse move input in either 'row,col' or alphanumeric (e.g., 'e4') format."""
    cmd = cmd.strip()
    
    # Try alphanumeric format first (e.g., 'e4' or 'E4')
    if len(cmd) >= 2:
        first = cmd[0].lower()
        if 'a' <= first <= 'o':
            try:
                col = ord(first) - ord('a')
                row = int(cmd[1:]) - 1  # Convert 1-indexed to 0-indexed
                if 0 <= row < 15:
                    return (row, col)
            except ValueError:
                pass
    
    # Fall back to 'row,col' format
    parts = cmd.split(",")
    if len(parts) == 2:
        try:
            row, col = int(parts[0]), int(parts[1])
            if 0 <= row < 15 and 0 <= col < 15:
                return (row, col)
        except ValueError:
            pass
    
    raise ValueError(f"Invalid move: {cmd}. Use 'row,col' (e.g., '7,7') or 'e4'")


def run_cli() -> None:
    """Run the CLI game loop."""
    runner = GameRunner()
    print("Gomoku Game - Standard 15x15")
    print("Enter moves as 'row,col' (e.g., 7,7) or 'e4' (alphanumeric)")
    print("Type 'quit' to exit, 'save' to save game, 'load' to load game")
    
    while True:
        print("\n" + format_board_simple(runner.game.board))
        print(f"Current player: {runner.game.current_player.value}")
        
        try:
            cmd = input("> ").strip()
            
            if cmd.lower() == "quit":
                print("Goodbye!")
                break
            
            if cmd.lower() == "save":
                with open("save.txt", "w") as f:
                    runner.save(f)
                print("Game saved to save.txt")
                continue
            
            if cmd.lower() == "load":
                try:
                    with open("save.txt", "r") as f:
                        runner.load(f)
                    print("Game loaded from save.txt")
                except FileNotFoundError:
                    print("No save file found")
                continue
            
            if cmd.lower() == "status":
                if runner.is_over():
                    winner = runner.get_winner()
                    if winner:
                        print(f"Winner: {winner}")
                    else:
                        print("Draw!")
                else:
                    print("Game ongoing")
                continue
            
            # Parse and make move using new parse_move function
            try:
                row, col = parse_move(cmd)
                runner.make_move(row, col)
            except ValueError as e:
                print(f"Error: {e}")
                continue
            
            if runner.is_over():
                print("\n" + format_board_simple(runner.game.board))
                winner = runner.get_winner()
                if winner:
                    print(f"Winner: {winner}")
                else:
                    print("Draw!")
                break
        
        except (ValueError, IndexError) as e:
            print(f"Invalid input: {e}")
        except KeyboardInterrupt:
            print("\nInterrupted!")
            break
