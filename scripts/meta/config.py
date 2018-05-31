from pathlib import Path, PosixPath
DEFAULT_KEY_PATH = Path('metadata', 'key.txt')

def read_default_api_key(keypath=DEFAULT_KEY_PATH):
    if type(keypath) is PosixPath and keypath.exists():
        return keypath.read_text().strip()
    else:
        return None


