#!/usr/bin/env bash
# both routes, separately and never pooled: ZF_REPO=<repo root> bash CFG242_run_all.sh
cd "$(dirname "$0")" && python3 CFG242_run_all.py AB
