#!/bin/bash
# CFG122 (door 4): re-run everything in place.  Needs numpy, scipy, sympy.  ZF_REPO = the repository root (read-only use: CFG7_common for the committed r_ta, CFG44 Bcommon for the S0.5 cross-check,
# superfluid_2026 and the pricing script for the post-hoc R5 row).  Total about 25 minutes on a 16-core machine (jobs run in parallel).
set -u
cd "$(dirname "$0")"
export ZF_REPO="${ZF_REPO:?set ZF_REPO to the repository root}"
python3 cfg122_s0_controls.py
python3 cfg122_g1a_scaling.py
python3 cfg122_g2.py
python3 cfg122_g3_virtualwork.py
python3 cfg122_g4_g5solar.py
python3 cfg122_g5_wellposed.py
MUTATE=b python3 cfg122_g5_wellposed.py
python3 cfg122_g6_twofluid.py
python3 cfg122_g1_plane.py &
MUTATE=a python3 cfg122_g1_plane.py &
MUTATE=c python3 cfg122_g1_plane.py &
python3 cfg122_g1_edge.py &
POSTHOC_ALPHA_HI=4 python3 cfg122_g1_edge.py &     # POST-HOC labelled: the alpha axis extended to 1e4 (not the frozen plane)
wait
python3 cfg122_posthoc_prior_art.py                # POST-HOC labelled: only after every gate run
python3 cfg122_summary.py > cfg122_summary.out
