# Reproduce

From the repository root, with Python3.13.9, NumPy1.26.4, SciPy1.14.1 and
SymPy1.13.1 as recorded, use fresh output directories:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 astra_goal_2026_11_05/AZ40_canonical_coupling/clock_repair/gradient_bound.py --out /tmp/az40-gradient-fresh
    python3 astra_goal_2026_11_05/AZ40_canonical_coupling/clock_repair/clock_math.py --out /tmp/az40-clock-fresh.json
    python3 astra_goal_2026_11_05/AZ40_canonical_coupling/clock_repair/clock_math.py --mutate --out /tmp/az40-clock-mutant-fresh.json
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 astra_goal_2026_11_05/AZ40_canonical_coupling/clock_repair/bianchi.py --out /tmp/az40-bianchi-fresh

Expected exits:0,0,1,0. The clock mutation fails6 checks intentionally.
Authoritative evidence is in evidence/gradient_verified, clock_main,
clock_mutate and bianchi. Their v2 manifests record complete command arguments,
input/output hashes, software, actual runtime and bounded execution. The raw
first failed radial run remains local at evidence/gradient; see the preserved
failure note and script. All mathematical scopes are in RESULT.md and the
pre-execution contracts. Scripts do not download or fit observational data.
