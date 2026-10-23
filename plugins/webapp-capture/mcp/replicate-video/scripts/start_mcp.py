#!/usr/bin/env python3
"""Contained executable entry point; does not require host-specific path macros."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from launch import main
main()
