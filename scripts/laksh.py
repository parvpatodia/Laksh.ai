#!/usr/bin/env python3
from __future__ import annotations

import argparse

from lakshai import __version__
from lakshai.pipeline.base import DummyPipeline


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("version")
    sub.add_parser("smoke")

    a = p.parse_args()

    if a.cmd == "version":
        print(__version__)
        return

    out = DummyPipeline().run([1, 2, 3])
    print("Output:", out)


if __name__ == "__main__":
    main()
