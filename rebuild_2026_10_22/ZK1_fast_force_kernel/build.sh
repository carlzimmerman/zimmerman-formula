#!/bin/bash
# ZK1: build the force kernel. Apple clang, M4. -ffast-math only licenses reordering the sum so the loop vectorises.
cd "$(dirname "$0")" && clang -O3 -ffast-math -mcpu=apple-m4 -shared -fPIC -o x48_force.dylib x48_force.c
