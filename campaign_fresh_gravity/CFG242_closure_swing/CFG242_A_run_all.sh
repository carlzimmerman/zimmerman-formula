#!/usr/bin/env bash
# route A: ZF_REPO=<repo root> bash CFG242_A_run_all.sh   (inside the repository the root is found by walking up)
cd "$(dirname "$0")" && python3 CFG242_run_all.py A
