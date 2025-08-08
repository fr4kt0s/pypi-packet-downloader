"""
Utilities for locating the newest file in a directory and delete files
"""

# Standard library imports

from pathlib import Path
from scripts.logger import logger


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
        raise FileNotFoundError(logger.warning(f"No files found in: {source_folder}"))

    # Choose the file with the greatest modification time
    return max(files, key=lambda f: f.stat().st_mtime)

def delete_file(file_path):
    """
    Tries to delete the specified file using pathlib with maximum error tolerance.
    Logs informative messages depending on the outcome.
    """
    try:
        # Convert to a Path object if necessary
        path = Path(file_path)

        # Check if the file exists before attempting to delete
        if not path.is_file():
            logger.warning(f"File does not exist: {path}")
            return

        path.unlink()
        logger.info(f"File successfully deleted: {path}")

    except PermissionError:
        logger.error(f"Permission denied: Cannot delete the file {path}.")
    except FileNotFoundError:
        # This can happen if the file is deleted between the check and unlink()
        logger.warning(f"File not found during deletion: {path}")
    except IsADirectoryError:
        logger.error(f"The specified path is a directory, not a file: {path}")
    except OSError as e:
        # Catch all other OS-related errors
        logger.error(f"OS error occurred while deleting the file {path}: {e}")
    except Exception as e:
        # Catch any other unexpected exceptions
        logger.exception(f"An unexpected error occurred while deleting {path}: {e}")

# Example usage:
# import logging
# logger = logging.getLogger(__name__)
# delete_file("example.txt", logger)
