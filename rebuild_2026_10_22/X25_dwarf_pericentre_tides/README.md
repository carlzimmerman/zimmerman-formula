# X25_dwarf_pericentre_tides: does the hosted-dwarf extra follow tidal stress at pericentre?

## Verdict

**TIDES RULED OUT AT PERICENTRE, on both footings, for the 31 MW ultra-faints with orbits on disk.** The 30 M31
systems of the hosted set have no orbit on disk. They keep X20's current-distance result, which is a lower bound on
their tidal stress.

X20's one qualifier was that τ used the current host distance. With Z2's PM-based pericentres:
- the extra over the isolated law (B_iso) does not rise with pericentric stress or with a tidal-heating proxy;
- the weakly stressed dwarfs carry the full extra.

| test (set P = 31 MW ultra-faints) | canonical | alt | JSON key |
|---|---|---|---|
| C1 Spearman(E, log τ_peri) ± boot; Kendall | −0.167 ± 0.179; −0.114 | −0.158 ± 0.181; −0.114 | `footings.<f>.C1` |
| C1 same-host permutation p (one-sided) | 0.51 | 0.50 | `C1.p_perm` |
| C2 Spearman(E, log H) (heating proxy) ± boot; Kendall | −0.093 ± 0.181; −0.067 | −0.095 ± 0.182; −0.071 | `footings.<f>.C2` |
| C2 permutation p | 0.34 | 0.35 | `C2.p_perm` |
| W τ_peri ≤ 0.1 (PRIMARY) | N 26, +0.602 ± 0.127, Z 4.8 **EXTRA** | N 26, +0.552 ± 0.126, Z 4.4 **EXTRA** | `W["0.1"]` |
| W τ_peri ≤ 0.03 | N 15, +0.596 ± 0.149, Z 4.0 EXTRA | N 15, +0.539 ± 0.149, Z 3.6 EXTRA | `W["0.03"]` |
| all of P | +0.596 ± 0.111 | +0.539 ± 0.111 | `all_P` |
| f_tid = 1 − Ẽ(τ_peri ≤ 0.1)/Ẽ(P), 68 % | −0.010 [−0.126, +0.026] | −0.025 [−0.136, +0.025] | `f_tid` |
| PC: E vs log M★, raw → partial at fixed τ_peri | −0.450 → −0.435 ± 0.170, p 0.017, **SURVIVES** | −0.465 → −0.451 ± 0.169, p 0.013, **SURVIVES** | `PC.logMstar` |
| PC: E vs log r_half, raw → partial | −0.342 → −0.304 ± 0.180, p 0.10, WEAKENED | −0.341 → −0.307 ± 0.179, p 0.10, WEAKENED | `PC.log_rhalf` |

- κ = ½ FITTED.
- The two footings are never pooled.
- This is not "theory closed". Nothing here says the data favour the framework.

**Checks 12/12 PASS.**
- K0: Step 0 reproduces X20 exactly on both footings: median τ, ρ, p, and the τ ≤ 0.1 subset N, median, sd and Z.
- K1: S1's host field reproduces X1's x_e to 0.
- K2: the orbit routine matches Kepler to 4e-9.
- K3: positive control, p = 5e-5.
- K4: negative control, 98.5 % of shuffles give p > 0.01.
- K5: peak memory 0.51 GB.
- K6: orbit sanity.

**MUTATE** (`X25_MUTATE=1`) swaps pericentre and apocentre. The named must-fail check K6 FAILS on both footings
(31/31 violations), and the run exits 1.

## What it says

- **The pericentre does raise the stress, but only modestly.** On P, the median τ goes from 0.0138 (current distance)
  to 0.0365 at pericentre (alt 0.0137 → 0.0379); the median ratio is 1.7. Still, 26 of 31 systems stay at τ_peri ≤ 0.1.
- **The extra does not follow stress.** Both rank correlations are slightly negative, and the permutation p is about 0.5.
  - The most stressed system, Boötes III (τ_peri 12, H 57), sits *below* the law (E −0.39 / −0.42).
  - The least stressed ones (Leo V, Pisces II, Eridanus II, Pegasus III; τ_peri ≤ 0.0023) carry +0.33 to +0.61.
- **The M★ trend is not a tidal proxy.**
  - At fixed τ_peri, the partial Spearman of E on log M★ barely moves (−0.45 → −0.44 / −0.47 → −0.45, permutation
    p 0.017 / 0.013).
  - log τ_peri and log M★ are nearly uncorrelated (+0.16 / +0.18).
  - The r_half trend is weaker to begin with (−0.34). It stays at −0.30 at fixed τ_peri, but p is 0.10.
- **Sensitivities (reported) all agree.** The weak subset stays EXTRA, and every Spearman is ≤ −0.09:
  - τ_grad (the |dg/dr| form): Z 4.9 / 4.4.
  - τ_max = max(τ_X20, τ_peri): Z 4.4 / 4.0.
  - Z2's closer 16th-percentile pericentres: Z 4.7 / 4.4.
  - The per-passage shock S₁: ρ −0.17 / −0.16.
- **LMC note (ledger A3).** For Pictor II, Carina II and Horologium I, X1's d_host is the distance to the LMC. Their
  X20 τ is therefore larger than their MW-pericentre τ. τ_max covers this.
- **M31 (no orbits on disk).** To reach τ = 0.1, the M31 systems would need r_p/d of 0.29 at the median (16–84 %:
  0.13–0.85). About half would need r_p < 0.3 d. Tides at pericentre are therefore not excluded for them by data.
  This lane cannot test them without M31 orbits.
- **What remains.** The hosted-dwarf requirement survives its last data-side loophole for the MW ultra-faints. The
  extra is not tidal, and it tracks M★ at fixed tidal stress.

## Files

- `FROZEN_CRITERIA.md` and `ASSUMPTION_LEDGER.md` (d4827bece5, committed alone, before any script or number).
- `x25_dwarf_pericentre_tides.py`.
- `.out` / `_results.json`, with the per-system τ_now, τ_peri, H, r_p and E in `footings.<f>.per_system`.
- `_MUTATE` outputs.

Run with:

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x25_dwarf_pericentre_tides.py                 # exit 0, 12/12
    X25_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x25_dwarf_pericentre_tides.py    # exit 1, K6 fails

Inputs (read-only): X1's `x1_per_system.csv`, Z2's `z2_per_system.csv` (orbits in S1's static MW field, no LMC), and
LVD `distance_gc` (used for K6 only).
