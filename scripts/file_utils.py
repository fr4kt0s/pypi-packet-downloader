"""
Utilities for locating the newest file in a directory and performing text replacements.
"""
# Standard library imports
import time
from datetime import datetime
from pathlib import Path


def get_latest_file(source_folder):
    """
    Return the most recently modified file in `source_folder`.

    Parameters:
        source_folder (str): Directory to search for the newest file.

    Returns:
        Path: Path object pointing to the latest file.

    Raises:
        FileNotFoundError: If the directory is empty.
    """
    files = list(Path(source_folder).glob("*"))
    if not files:
        raise FileNotFoundError(f"No files found in {source_folder!r}")
    # Choose the file with the greatest modification time
    return max(files, key=lambda f: f.stat().st_mtime)
