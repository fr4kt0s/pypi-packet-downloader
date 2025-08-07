import sys
import subprocess
import os

MIRROR_BASE = "/mnt/python/data"  # oder beliebiges Zielverzeichnis


def main():
    if len(sys.argv) < 2:
        print("Kein Paketname übergeben", file=sys.stderr)
        sys.exit(1)

    package = sys.argv[1]
    print(f"Starte Download für Paket: {package}")

    # Aufruf von bandersnatch mit einem Include-Filter für das spezifische Paket
    try:
        result = subprocess.run([
            "bandersnatch",
            "--config", "/opt/python/pypi-packet-downloader/config/bandersnatch.conf",
            "sync", package
        ], capture_output=True, text=True, check=True)

        print("Bandersnatch-Ausgabe:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Fehler bei bandersnatch:", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(2)

if __name__ == '__main__':
    main()