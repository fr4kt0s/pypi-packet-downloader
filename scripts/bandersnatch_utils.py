import subprocess
import os

def mirror_package(package_name: str, config_path: str = None) -> str:
    if config_path is None:
        # Standardpfad relativ zur main.py
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'bandersnatch.conf')
        config_path = os.path.abspath(config_path)

    try:
        result = subprocess.run(
            ["bandersnatch", "--config", config_path, "sync", package_name],
            capture_output=True,
            text=True,
            check=True
        )
        return f"Bandersnatch erfolgreich ausgeführt für Paket '{package_name}'.\n\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        error_message = f"Fehler beim Ausführen von bandersnatch für Paket '{package_name}':\n{e.stderr}"
        raise RuntimeError(error_message) from e