#!/usr/bin/env python3
"""Save your Replicate API token once, in a private file outside every project.

Run it yourself in a terminal (typing is hidden):
  python3 set_token.py            # asks for the token
  python3 set_token.py --check    # also confirms it works with one read-only request
  python3 set_token.py --remove   # deletes the saved token
  python3 set_token.py --where    # shows where the file lives (never the token)
Get a token at https://replicate.com/account/api-tokens. Never paste it into a chat.
Designed by Legion Code Inc.
"""
import argparse
import getpass
from pathlib import Path
import sys
import urllib.error
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from token_store import TOKEN, read_token, token_path, write_token


def check(value):
    request = urllib.request.Request("https://api.replicate.com/v1/account", headers={"Authorization": f"Bearer {value}"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status == 200
    except urllib.error.HTTPError as error:
        return False if error.code in (401, 403) else None
    except OSError:
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="confirm the token with one read-only request to Replicate")
    parser.add_argument("--remove", action="store_true", help="delete the saved token file")
    parser.add_argument("--where", action="store_true", help="print where the token file lives")
    parser.add_argument("--stdin", action="store_true", help="read the token from standard input (for scripts)")
    args = parser.parse_args()
    path = token_path()
    if args.where:
        print(f"{path} ({'saved' if read_token(path) else 'no token saved'})")
        return 0
    if args.remove:
        path.unlink(missing_ok=True)
        print(f"Removed {path}. Restart Claude or ChatGPT so the video tools stop using it.")
        return 0
    value = (sys.stdin.readline() if args.stdin else getpass.getpass("Paste your Replicate API token (typing is hidden): ")).strip()
    if not TOKEN.match(value):
        print("ERROR: that does not look like a Replicate token (they start with r8_). Nothing was saved.", file=sys.stderr)
        return 1
    if args.check:
        ok = check(value)
        if ok is False:
            print("ERROR: Replicate rejected that token. Nothing was saved.", file=sys.stderr)
            return 1
        print("Replicate accepted the token." if ok else "Could not reach Replicate to check; saving anyway.")
    saved = write_token(value, path)
    print(f"Saved to {saved} (only you can read it). Restart Claude or ChatGPT, then run the production doctor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
