from pathlib import Path


def read_file(file_path):
    path = Path(file_path)
    try:
        return path.read_text(encoding="utf-8").lower()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return ""
