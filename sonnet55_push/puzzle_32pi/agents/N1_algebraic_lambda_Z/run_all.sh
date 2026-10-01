#!/bin/sh
set -e
cd "$(dirname "$0")"
sha256sum -c PREDECLARED.sha256 2>/dev/null || shasum -a 256 -c PREDECLARED.sha256
python3 n01_menu.py > n01_menu.out
python3 n02_confront.py > n02_confront.out
tail -1 n01_menu.out n02_confront.out
