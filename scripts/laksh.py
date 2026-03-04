#!/usr/bin/env python3
import argparse
from lakshai.pipeline.base import DummyPipeline
from lakshai import __version__

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('version')
    sub.add_parser('smoke')
    a = p.parse_args()
    if a.cmd == 'version':
        print(__version__)
    else:
        out = DummyPipeline().run([1,2,3])
        print('Output:', out)

if __name__ == '__main__':
    main()
