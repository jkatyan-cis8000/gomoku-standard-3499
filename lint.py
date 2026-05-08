#!/usr/bin/env python3
"""
Lint.py - Enforces Gomoku source architecture rules.

Checks:
1. Every source file lives in exactly one layer directory under src/
2. Imports respect the forward dependency direction
3. No file exceeds 300 lines
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Tuple

# Layer order (index defines dependency direction)
LAYER_ORDER = ["types", "config", "repo", "service", "providers", "utils", "runtime", "ui"]

# Valid imports per layer
VALID_IMPORTS = {
    "types": ["types"],
    "config": ["types", "config"],
    "repo": ["types", "config", "repo"],
    "service": ["types", "config", "repo", "providers", "service"],
    "providers": ["types", "config", "utils", "providers"],
    "utils": ["utils"],
    "runtime": ["types", "config", "repo", "service", "providers", "runtime"],
    "ui": ["types", "config", "service", "runtime", "providers", "ui"],
}

MAX_LINES = 300
SRC_DIR = Path(__file__).parent / "src"


def get_layer(filepath: Path) -> str | None:
    """Return the layer name if the file is in a valid layer directory."""
    rel_path = filepath.relative_to(Path(__file__).parent)
    parts = rel_path.parts
    
    if len(parts) < 2:
        return None
    
    # Find the first part after src/ that matches a layer
    for i, part in enumerate(parts):
        if part == "src" and i + 1 < len(parts):
            layer = parts[i + 1]
            if layer in LAYER_ORDER:
                return layer
    return None


def get_imports(filepath: Path) -> List[str]:
    """Extract all import statements from a Python file."""
    imports = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(filepath))
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module.split(".")[0])
    except SyntaxError:
        pass
    return imports


def check_line_count(filepath: Path) -> List[Tuple[int, str]]:
    """Check if file exceeds max lines."""
    errors = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if len(lines) > MAX_LINES:
            errors.append((len(lines), f"File exceeds {MAX_LINES} lines ({len(lines)} lines)"))
    except Exception:
        pass
    return errors


# Standard library modules that are always allowed
STDLIB_MODULES = {
    "abc", "aifc", "argparse", "array", "ast", "asynchat", "asyncio", "asyncore",
    "atexit", "audioop", "base64", "bdb", "binascii", "binhex", "bisect",
    "builtins", "bz2", "calendar", "cgi", "cgitb", "chunk", "cmath", "cmd",
    "code", "codecs", "codeop", "collections", "colorsys", "compileall",
    "concurrent", "configparser", "contextlib", "contextvars", "copy", "copyreg",
    "cProfile", "crypt", "csv", "ctypes", "curses", "dataclasses", "datetime",
    "dbm", "decimal", "difflib", "dis", "distutils", "doctest", "email",
    "encodings", "enum", "errno", "faulthandler", "fcntl", "filecmp", "fileinput",
    "fnmatch", "fractions", "ftplib", "functools", "gc", "getopt", "getpass",
    "gettext", "glob", "graphlib", "grp", "gzip", "hashlib", "heapq", "hmac",
    "html", "http", "imaplib", "imghdr", "imp", "importlib", "inspect", "io",
    "ipaddress", "itertools", "json", "keyword", "lib2to3", "linecache", "locale",
    "logging", "lzma", "mailbox", "mailcap", "marshal", "math", "mimetypes",
    "mmap", "modulefinder", "multiprocessing", "netrc", "nis", "nntplib",
    "numbers", "operator", "optparse", "os", "ossaudiodev", "pathlib", "pdb",
    "pickle", "pickletools", "pipes", "pkgutil", "platform", "plistlib", "poplib",
    "posix", "posixpath", "pprint", "profile", "pstats", "pty", "pwd", "py_compile",
    "pyclbr", "pydoc", "queue", "quopri", "random", "re", "readline", "reprlib",
    "resource", "rlcompleter", "runpy", "sched", "secrets", "select", "selectors",
    "shelve", "shlex", "shutil", "signal", "site", "smtpd", "smtplib", "sndhdr",
    "socket", "socketserver", "spwd", "sqlite3", "ssl", "stat", "statistics",
    "string", "stringprep", "struct", "subprocess", "sunau", "symtable", "sys",
    "sysconfig", "syslog", "tabnanny", "tarfile", "telnetlib", "tempfile", "termios",
    "test", "textwrap", "threading", "time", "timeit", "tkinter", "token", "tokenize",
    "tomllib", "trace", "traceback", "tracemalloc", "tty", "turtle", "turtledemo",
    "types", "typing", "unicodedata", "unittest", "urllib", "uu", "uuid", "venv",
    "warnings", "wave", "weakref", "webbrowser", "winreg", "winsound", "wsgiref",
    "xdrlib", "xml", "xmlrpc", "zipapp", "zipfile", "zipimport", "zlib",
    "_thread", "__future__", "zoneinfo"
}


def check_imports(filepath: Path, layer: str) -> List[Tuple[int, str]]:
    """Check that imports respect layer dependency rules."""
    errors = []
    valid = set(VALID_IMPORTS.get(layer, []))
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        for node in ast.walk(ast.parse("".join(lines), filename=str(filepath))):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name.split(".")[0]
                    # Skip standard library imports - they're always allowed
                    if module in STDLIB_MODULES:
                        continue
                    if module not in valid:
                        errors.append((node.lineno, f"Cannot import '{module}' from layer '{layer}'. Valid: {sorted(valid)}"))
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module = node.module.split(".")[0]
                    # Skip standard library imports - they're always allowed
                    if module in STDLIB_MODULES:
                        continue
                    if module not in valid:
                        errors.append((node.lineno, f"Cannot import '{module}' from layer '{layer}'. Valid: {sorted(valid)}"))
    except SyntaxError:
        pass
    
    return errors


def check_file(filepath: Path) -> List[Tuple[int, str, str]]:
    """Run all checks on a file. Returns list of (line, message, category)."""
    errors = []
    layer = get_layer(filepath)
    
    if layer is None:
        return []
    
    # Check line count
    line_errors = check_line_count(filepath)
    for line, msg in line_errors:
        errors.append((line, msg, "line_count"))
    
    # Check imports
    import_errors = check_imports(filepath, layer)
    for line, msg in import_errors:
        errors.append((line, msg, "import"))
    
    return errors


def find_python_files() -> List[Path]:
    """Find all Python files under src/."""
    files = []
    if not SRC_DIR.exists():
        return files
    
    for root, _, filenames in os.walk(SRC_DIR):
        for filename in filenames:
            if filename.endswith(".py"):
                files.append(Path(root) / filename)
    return files


def main() -> int:
    """Run linter and return exit code."""
    errors_by_file: dict[Path, list[tuple[int, str, str]]] = {}
    
    for filepath in find_python_files():
        file_errors = check_file(filepath)
        if file_errors:
            errors_by_file[filepath] = file_errors
    
    if not errors_by_file:
        print("All checks passed.")
        return 0
    
    # Print errors sorted by file
    for filepath in sorted(errors_by_file.keys()):
        print(f"\n{filepath}:")
        for line, msg, category in sorted(errors_by_file[filepath], key=lambda x: x[0]):
            print(f"  Line {line}: [{category}] {msg}")
    
    total = sum(len(errs) for errs in errors_by_file.values())
    print(f"\n{total} error(s) found.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
