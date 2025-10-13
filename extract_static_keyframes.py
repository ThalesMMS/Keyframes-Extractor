#!/usr/bin/env python3
"""Compatibility wrapper for the static keyframe extractor CLI."""

from __future__ import annotations

import sys

from static_keyframe_extractor.cli import main


if __name__ == "__main__":
    sys.exit(main())
