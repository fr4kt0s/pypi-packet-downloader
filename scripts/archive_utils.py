"""
Utilities for packaging a list of files into a timestamped tar.gz archive.
"""
# Standard library imports
import os
import time
import tarfile
from datetime import datetime
from pathlib import Path


def create_archive(latest_file, package_name, output_folder):
    """
    Read file paths from `modified_list_path` and build a .tar.gz archive.

    Parameters:
        latest_file (Path or str):
            Text file containing one file path per line.

        output_folder (str):
            Directory where the resulting archive will be saved.
        package_name (str):
            Name of the given package
    Returns:
        Path: Full path to the newly created archive.

    Raises:
        FileNotFoundError: If any listed file does not exist.
        :param latest_file:
        :param output_folder:
        :param package_name:
    """
    # Build a timestamp for the archive name
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    archive_name = f"{package_name}_{date_str}.tar.gz"
    archive_path = Path(output_folder) / archive_name

    # Load all non-empty lines (file paths) from the modified list
    with open(latest_file, encoding='utf-8') as f:
        paths = [line.strip() for line in f if line.strip()]

    # Create compressed tar.gz, preserving folder structure
    with tarfile.open(archive_path, "w:gz") as tar:
        for p in paths:
            if os.path.isfile(p):
                # Compute path inside archive relative to SOURCE_FOLDER
                arcname = os.path.relpath(p, start="/mnt/python/")
                tar.add(p, arcname=arcname)
            else:
                # Abort if a path is missing
                raise FileNotFoundError(f"Cannot archive missing file: {p}")

    return archive_path