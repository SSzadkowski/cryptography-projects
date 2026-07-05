from pathlib import Path


def read_ascii_text(filename):
    try:
        return Path(filename).read_text(encoding="ascii")
    except UnicodeDecodeError as e:
        raise ValueError("Plik musi zawierać tylko znaki ASCII.") from e