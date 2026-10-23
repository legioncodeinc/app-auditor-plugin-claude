"""Per-user Replicate token file, so nobody has to edit shell profiles or paste a key in chat.

The file lives outside every project (default ~/.config/webapp-capture/replicate.env, or
$XDG_CONFIG_HOME/webapp-capture/replicate.env, or WEBAPP_CAPTURE_TOKEN_FILE), is owner-only,
and is never read through a symlink or when other users can read it. An environment
variable always wins over the file. Designed by Legion Code Inc.
"""
import os
from pathlib import Path
import re
import stat
import sys

KEY = "REPLICATE_API_TOKEN"
TOKEN = re.compile(r"^r8_[A-Za-z0-9]{20,}$")


def token_path():
    if os.environ.get("WEBAPP_CAPTURE_TOKEN_FILE"):
        return Path(os.environ["WEBAPP_CAPTURE_TOKEN_FILE"]).expanduser()
    base = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return base / "webapp-capture" / "replicate.env"


def read_token(path=None):
    """Return the stored token, or None. Never raises and never prints the value."""
    path = Path(path or token_path())
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    except OSError:
        return None
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o077 or (hasattr(os, "getuid") and info.st_uid != os.getuid()):
            print(f"webapp-capture: ignoring {path}: it must be a regular file only you can read (chmod 600).", file=sys.stderr)
            return None
        text = os.read(fd, 4096).decode("utf-8", "replace")
    finally:
        os.close(fd)
    for line in text.splitlines():
        name, _, value = line.partition("=")
        if name.strip() == KEY and value.strip():
            return value.strip().strip('"').strip("'")
    return None


def write_token(value, path=None):
    """Write the token owner-only. Refuses symlinks. Returns the path."""
    path = Path(path or token_path())
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if path.parent.is_symlink() or path.is_symlink():
        raise SystemExit(f"ERROR: refusing to write through a symlink at {path}")
    os.chmod(path.parent, 0o700)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.fchmod(fd, 0o600)
        os.write(fd, f"{KEY}={value}\n".encode())
    finally:
        os.close(fd)
    return path


def load_into_environment():
    """Launcher hook: fill the environment from the file only when the variable is unset."""
    value = os.environ.get(KEY, "")
    if value.startswith("${") or not value.strip():
        os.environ.pop(KEY, None)
        stored = read_token()
        if stored:
            os.environ[KEY] = stored
