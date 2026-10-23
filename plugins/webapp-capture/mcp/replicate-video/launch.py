#!/usr/bin/env python3
"""Portable launcher: each user supplies their own credential, from the environment or from
the owner-only token file written by scripts/set_token.py."""
from token_store import load_into_environment

def main():
    # An unexpanded host placeholder such as ${user_config...} counts as unset.
    load_into_environment()
    from server import main as serve
    serve()

if __name__ == "__main__":
    main()
