# Depth-N Escalating Forced-Interlock Sweep — VERDICT (depths 6, 7, 8)

Script: `exhaust_depthN_forced.py` (depth-parametric, D>=6; imports depth-5 machinery verbatim).
Run mode: per-depth heads (completeness + soundness self-check, a0-validity) then the full 21-target
constructive sweep via `--workers 12`. RULE 3 held throughout: **zero git diff** on
`gate/ engine/ exhaust.py exhaust_parallel.py exhaust_depth4_forced.py exhaust_depth5_forced.py`.
No git commit. HARD 6 GB watchdog cap, never raised.

## Per-depth ledger

| D | splits | raw/target | distinct values | in-window hits | CERT | RELAB | peak RSS | wall | verdict |
|---|--------|-----------:|----------------:|---------------:|:----:|:-----:|---------:|------|---------|
| 6 | (1,4)(2,3) | 236,624 | 107,719 | 259 | 0 | 0 | 0.35 GB/worker | 13.2 s | CLEAN NULL |
| 7 | (1,5)(2,4)(3,3) | 1,566,116 | 498,848 | 1,248 | 0 | 0 | 1.38 GB/worker | 95.3 s | CLEAN NULL |
| 8 | (1,6)(2,5)(3,4)(4,3) | 8,123,807 | 2,207,173 | (single-target probe) | 0 | 0 | **5.77 GB single-proc / 11.5+ GB parallel** | 515 s/target | **WALL** |

Heads (each depth, exit 0):
- **Completeness**: per-split skeleton cross-check scheme==brute, 0 missed/0 extra
  (D6: 13/73; D7: 13/73/247; D8 b_s=4 split independently verified 1147==1147, 0/0, 227 s) +
  committed depth-4 anchor 11,209==11,209. `CONSTRUCTIVE_COMPLETE=True` at 6, 7, 8.
- **Soundness**: 300/300 sampled candidates pass keep-predicate AND real `gate.forced_kernel` at D6, D7.
- **a0-validity**: LEG1 re-finds a0=((c/Z)*H_L)=9.36018e-11 (rel_err 1.97e-5); LEG2 depth-D a0xidentity
  tree == a0 (L/T^2), gate FDR-DEAD (expected). PASS at D6, D7, D8.

## Both-ways reading
Every depth is a **CLEAN NULL, gates FIRING** — the expected/valid outcome. In-window hits exist and
grow with depth (259 -> 1,248) but ALL die at Gate A (FDR). No CERTIFIED, no RE-LABELED survivor —
NOT a win, NOT a manufactured dismissal. Tightest hit at both D6 and D7:
`koide_Q_lep` rel_err 9.23e-6, kernel PASS (B=True), interlock C=False, killed **FDR-DEAD @ GATE A**
(E_chance=0.0824 sparse; surplus -0.0 bits < 10-bit threshold, x21 look-elsewhere). Expected.

## The wall: **wall_depth = 8** (feasibility ceiling)
Depth 7 is the **last cleanly runnable depth** (parallel sweep 1.38 GB/worker, 95 s, full validation).
Depth 8 walls on TWO independent constraints:

1. **Memory (operative for the required parallel-sweep mode).** A single depth-8 build peaks at
   **5.77 GB** (max RSS 6,198,444,032 B; peak footprint 6,160,470,960 B) — 96% of the 6 GB cap, zero
   headroom. The sweep launches 12 detached workers, each building its OWN 2.2M-value/5.77 GB set:
   measured **11.5 GB combined after only 90 s** (builds ~15% done), memory compressor active, projected
   to ~69 GB at build peak — the exact 64 GB->swap thrash the memory brief forbids. Killed before swap
   damage. Depth 8 is un-runnable in the required `--workers` configuration.
2. **Time.** 515 s (8.6 min) for the build of a SINGLE target; the depth-8 completeness cross-check
   costs ~227 s for the b_s=4 split alone. A serial whole-sweep exceeds the ~15 min/depth budget.

Depth 9 (raw 38.5M, ~4.7x depth 8) is hopeless on both axes even single-process, and its b_s=5
completeness cross-check (~40 min) makes validation itself infeasible.

Note: the single-process 5.77 GB is TIGHTER than the spec's ~7.15 GB projection because the depth-8
value dedup was far better than projected (2.21M distinct vs the projected 3.70M). The wall lands at
depth 8 either way — the parallel-sweep memory breach is decisive and empirically demonstrated.

## RULE 3
`git diff` on gate/ engine/ exhaust.py exhaust_parallel.py exhaust_depth4_forced.py
exhaust_depth5_forced.py = EMPTY (clean) at start, mid-run, and end. Only new untracked files added.
