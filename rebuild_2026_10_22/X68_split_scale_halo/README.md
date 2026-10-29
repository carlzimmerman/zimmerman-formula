# X68_split_scale_halo

**Question.** The external model's T1 (relayed by the owner, 10-29) was to split X43's Burkert halo into an inner core r_c and
an outer infall scale r_s:

ρ = Σ_core r_s² / ((r + r_c)(r² + r_s²)), with r_s = max(r_c, r_f/c_f).

The aim was to give cluster outskirts more mass without new constants. Criteria were frozen first (d090d6b552).

## Verdict: SS UNDECIDED [c_f EXTERNAL], both footings

**100 % fallbacks.** The frozen hypothesis has no solution for any halo. With Σ_core fixed by X43's rule and r_s = r_f/c_f:

- even the r_c → 0 split halo already holds more than the halo's mass;
- every SPARC galaxy, group and cluster therefore fell back to X43's Burkert;
- the graded numbers are X43's exactly: groups Z +2.05, G-OUT-M3 Z +2.41, everything else passing;
- the mutation is harness-insensitive for the same reason.

Post-hoc diagnostic (canonical):

| system | r_f/c_f ÷ Burkert r₀ (median) | mass of r_c → 0 split halo ÷ target (median) |
|---|---|---|
| SPARC | 2.4 | 5.5 |
| groups | 1.4 | 2.5 |
| clusters | 2.2 | 4.9 |

**Why.** The halo's mass is fixed: the fair share inside r_ta for clusters, EM1's M200 for galaxies and groups. A profile
that holds ρ ≈ Σ/r out to r_s = r_f/c_f carries about 2πΣ r_s² ln(1 + R²/r_s²). At Σ_core that is 2.5–5.5 × too much.

The proposal's quoted "×3–5 more outer mass at fixed ρ₀r_c" is that same excess. It cannot be added to a halo of fixed
mass. More outer mass must be paid for by a lower inner surface density, and that contradicts the core rule.

## Reported, not graded: the proposal's own r_s = (Σ_core/Σ_M) r_c (canonical only)

| metric | result |
|---|---|
| SPARC | 0.0776, line PASS |
| groups | Z +1.83, **CONSISTENT** (X43: +2.05) |
| G-OUT-M3 | no longer failing |
| cluster keys that now fail | G-IN-all, G-MID-T1, G-IN-Mall, all **OVER** |

This is the same trade in a feasible form. Mass moved outward at a fixed Σ forces a smaller r_c and a denser centre, so
the inner bands overshoot. It also ties the outer halo to a₀, which is why it was not the frozen choice.

**Reading.** Where the halo's mass sits is a zero-sum budget. X43's two misses (groups and heavy-cluster outskirts) ask for
more mass outside the core. Every way of adding it at a fixed core surface density over-densifies the centre (X68's reported
variant), and the record's IB1 / X48 inner-band results already lean OVER. A real fix must lower the inner Σ in heavy
halos while raising the outer mass. Under the max() rule, that means a different collapse-branch η·Σ_coll, not a reshaped
profile.

κ = ½ FITTED; c_f EXTERNAL; not theory closed.

## Files and reproduction

Files: `FROZEN_CRITERIA.md`, `x68_split_scale.py`, `.out` / `_results.json`, `_MUTATE` versions, `x68_x30_machinery*.log`.
Checks 10/10, including K0x43 (split off reproduces X43 exactly, max |d| = 0).

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x68_split_scale.py            # ~70 s, exit 0
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x68_split_scale.py --mutate   # r_s doubled

The post-hoc fallback diagnostic was added after the first run showed 100 % fallbacks. It reports only and changes no
graded number.
