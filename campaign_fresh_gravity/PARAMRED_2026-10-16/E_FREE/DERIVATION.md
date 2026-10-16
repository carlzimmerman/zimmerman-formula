# Lane E (FREE): what the conditions force, and what they do not

Verdict: **CONSTRAINT TIGHTENED** (three families killed, one selector family shown infeasible under its own gates, no input removed).
Files: `FROZEN_CRITERIA.md` (written first), `CONDITIONS.md`, `e_free_intersection.py`, `e_free_results.json` / `e_free.out`,
`e_free_results_MUTATE.json` / `e_free_MUTATE.out`. All numbers below are read from the JSON unless marked "hand".
kappa = 1/2 FITTED; Omega_c/Omega_b = 5.364 measured; both footings, never pooled; not "theory closed".

## 1. The three questions

| question | answer | why |
|---|---|---|
| (i) Do the conditions pin one functional form for UFDs, early types and clusters? | **NO** | universal F: E and C intervals do not intersect (gap x19.1); a single power law in M_b is excluded; the hot-gas form covers E and C but not U |
| (ii) Is there a family with at most one constant expressible through a0, Sigma_bar, M_b, tether binding, c_s(T_IGM)? | **NO** | no dimensionless combination of (G, a0, M_b) exists; the E-C break sits at V_flat ~ 170-1100 km/s, 10-94x above c_s(T_IGM); at least one extra scale or a baryon-state variable is needed |
| (iii) Do the conditions force sqrt2 and R_ind of CFG782? | **NO** | the V_th window is EMPTY for every multiplier, every T_IGM and both footings (L/U = 1.320); R_ind is an external chemistry input that is load-bearing (R_ind = 1 moves the window to (4.60, 5.25] km/s) |

## 2. Derivation of the family the conditions allow

**Step 1, the genus (from W3, N2-N6, N3).** The free component must be untethered (W3, CFG776), collisionless (N3), not made by tether overflow (N5),
P-wave export or heating (N6), a capture channel (N2) or conversion (N7). Its only conserved source is the cold energy attached to baryons that
left the basin, so for a system i

  M_free,i = F_i S_i,   S_i = (Omega_c/Omega_b) (1/f_i - 1) M_b,i,   0 <= F_i <= 1   (N4),

with f_i the catchment retention (census CFG416/804; CFG806 could not derive it, so it is a data function, not a constant).

**Step 2, needed F per class (T2, formulas in FROZEN_CRITERIA.md section 3).**

| class | needed | F interval | source |
|---|---|---|---|
| U (UFD) | M_free(<r)/M_law(<r) = 10^(2 delta) - 1 = 3.47 [1.91, 5.85], i.e. 68.6 M_b [19.9, 225.5] inside r | LOWER bound only: F_U >= 0.0318 (leaky-box R_ind = 10^2.07), 0.1277 (R_ind 6-30), 0.0008 (R_need 10^3.65) | CFG28, 336, 317 |
| E (early types, log M* 10.8) | 0.55-0.80 M* over S_E = 24.7-48.3 M_b (N = 5.6-10) | F_E in [0.0114, 0.0324] if late types carry F = 0 | CFG745, 804 |
| C (clusters) | X-COP 3.0 (1.9-4.5) M_b over S_C = 2.46-3.07 M_b (f_eff 0.636-0.686) | F_C in [0.619, 1.0] (raw upper 1.83 cut by the cap) | CFG745, 814 |

Intersections: E-C **empty**, gap C_lo/E_hi = **19.1**; U-C non-empty; U-E touches only at F = 0.0318-0.0324 (2% margin, primary accounting, not robust);
joint (U, E, C) **empty**. The early-late differential gives the same verdict independently: a universal rule predicts +0.013 against +0.280 +- 0.083
(Z 3.22); the frozen linear form would need F = 15.2-27.9 against the cap 1. (Read-through, post-freeze: the linear form is only a restatement of
CFG811's own Z; the verdict does not depend on it.) Prior art with the same shape: CFG59 (one multiplier phi, NO, SLUGGS phi >= 0.81 vs M31 LVD <= 0.30).

**Step 3, no power law (T4).** With log M_b = 3.95 (UFD median), 10.8 (E), 13.0-14.0 (C): the E->C segment needs p in [0.40, 0.88]; the U->E segment allows
p <= 0.001 (primary), <= -0.087 (R_ind 6-30), <= 0.232 (most generous). The ranges never meet, so F(M_b) needs a break between M* 10^10.8 and the
cluster scale. Any monotone variable (M_b, V_flat, tether binding energy) gives the same conclusion because all are monotone in M_b.

**Step 4, the break needs a new scale (T5).** The exponent matrix of (G, a0, M_b) in (L, M, T) has null space dimension 0, so no dimensionless variable
can be built from the framework quantities alone. Adding c or c_s gives exactly one: V_flat/c or V_flat/c_s, V_flat = (G M_b a0)^(1/4)
(control: (G, M, r, c) returns the single combination G M/(r c^2), up to a scalar). The break lies between V_flat = 167.3 (canonical; 175.4 alt) at E and
593.7-1055.8 (622.5-1107.0 alt) at C, while c_s(T_IGM) = 11.8-16.7 km/s (T 1-2e4 K). So the IGM temperature cannot set it. Hand arithmetic with
T_vir = mu m_p V^2/(2k), mu 0.59: ~1.0e6 K at E, ~1.3e7-4.0e7 K at C, i.e. the onset of an X-ray halo, which is CFG745's baryon-state variable (hot-gas
fraction) and agrees with CFG741's independent statement that the selector needs a velocity scale ~250-700 km/s or a gas-state dependence. This is
a consistency remark, not a derivation of the scale.

**Step 5, the hot-gas family (T3).** M_free = k M_hot (CFG745, k = 2.88-3.62) is the only on-record form that covers C (by construction) and E (a pending sealed
prediction, CFG746) with one constant. As stated (present hot gas) it gives UFDs zero free mass against a requirement of >= 19.9 M_b: **violated**. Only
under a post-hoc "ever-hot" reading does it admit UFDs, and then k_U >= 0.169 is a lower bound (unconstrained above) and R_ind re-enters. k/5.364 = 0.54-0.67 is
the statement F_C ~ 0.6-1 restated; it is not an independent coincidence and is not used.

**Step 6, the selector (T1).** For V_init = (G R_ind M_b a0)^(1/4) with the CFG317 inputs (97 objects with R_ind; OLS log R_ind = +3.387 - 0.343 log M_b):

| footing | S1 needs V_th > | set by | S2 needs V_th <= | set by | window | L/U |
|---|---|---|---|---|---|---|
| canonical | 15.09 km/s | Bootes I (27th of 30 UFDs) | 11.43 km/s | Andromeda XXII (M31 LVD, 2 of 29 allowed) | EMPTY | 1.320 |
| alt | 15.82 | Bootes I | 11.99 | Andromeda XXII | EMPTY | 1.320 |

M31 Collins alone gives V_th <= 12.86 (And XI), also below L. Four Collins and eight LVD objects have V_init < L (And XI, XIII, XV, XVII, XX, XXII, XXVI,
Cas II among LVD; And XI, XX, XXII, XXVI among Collins). Because both footings scale V by a0^(1/4), L/U is footing-independent. Hence **no** multiplier lambda
(sqrt2 or otherwise) and no T_IGM rescues the frozen gates; the failure is not a tuning issue. Controls: K1 reproduces CFG782's five group fractions to
1e-9; MUTATE (R_ind = 1) moves the window to (4.60, 5.25], so R_ind is load-bearing.

Post-hoc diagnostic (not a test): the window opens at (13.3, 13.5] for S1 >= 0.8 with S2 <= 0.2, at (15.1, 15.6] for S1 >= 0.9 with S2 <= 0.3, i.e. only
with widths of 0.2-0.5 km/s (1.5-3%) and a relaxed S2. If S2 is applied only to MW classicals and the LV field, the window is (15.09, 20.80] and contains
sqrt2 c_s at 1e4 K (16.73) and 1.5e4 K (20.49) but not 2e4 K (23.66). So the selector is dead only because the faint M31 dwarfs are required to carry no
free cold energy. That requirement was scored on population fractions, not per object (CFG784 was not run by its frozen conditional; the M31 LVD
population offset +0.0435 dex, CFG91, is a median dominated by brighter dwarfs).

## 3. Named conflicts (which postulate must be dropped)
1. **P1: CFG745/804 (early types) vs CFG745/814 (clusters)**: one universal free fraction of the expelled cold energy is impossible. The H-EX form
   (CFG808-815) survives only for clusters.
2. **P2: CFG811 vs CFG669 (and CFG810)**: expelled-share at galaxy scale is wrong on both sides (too much mass for the average galaxy, +443;
   too little early-late contrast, +0.013 vs +0.280). The early-type case of S4 has no surviving expelled-share form; merger memory also fails (CFG726).
3. **P3: CFG28/259 (UFD offset) with CFG782 S1/S2**: the V_init-threshold selector with CFG317 inputs is infeasible; drop or re-gate it.
4. **P4 (ledger-derived, not recomputed): CFG817 middle tercile x1.59 vs CFG647/804 cap vs CFG818/819 placement**: inside H-EX, no extra mass and no
   re-placement is available.
5. **P5: eRASS1 vs ACCEPT (CFG727, CFG815)**: tercile pattern 1.27 / 1.59 / 0.96 is non-monotonic in mass; F depends on a second variable.

## 4. Argued, not demonstrated: the tidal-debris clause of S4 looks like a corollary
CFG749 shows cold energy moving relative to the baryons at >= 0.3 V_flat is unbound (self-gravity cancelled by the tether), and CFG744/760-762 close every
capture channel. Debris formed with v_rel ~ 100-200 km/s through resting cold energy has v_rel/(0.3 V_flat) ~ 6-20 for a 1e8-1e9 M_sun dwarf
(V_flat 33-59 km/s, hand arithmetic, masses assumed). So "captures none" would follow without a third postulate. Not computed in this lane and not counted
as a result. It competes with the formation clock (CFG763): they agree for young tidal dwarfs and differ for old ones (clock >= 68% filled by 4 Gyr; no
capture, 0 forever). NGC 5557-E1 (Newton 16-24 vs law 28-41 km/s, needs +-4) decides.

## 5. What observation decides each open item
- Per-object dispersions of the flagged M31 dwarfs (4 Collins + 8 LVD, overlapping; law vs law + free): decides whether CFG782's death is a data kill or a gate artefact. A restricted CFG784 run; the dispersions were already used by CFG59 and CFG91.
- M_hot(<100 kpc) of log M* 10.8 quiescent galaxies by SZ / X-ray stacking (sealed CFG746: 1.1-1.6e10 M_sun, falsifier less than half): decides the hot-gas form for E.
- NGC 5557-E1 kinematics: decides capture vs clock.
- A per-cluster condensed fraction / outskirt gas slope beyond 2 r200m for the 318 eRASS1 clusters: the middle-tercile conflict (P4) cannot be separated from census
  uncertainty without it.

## 6. Limits and the strongest objection
- Strongest objection: F_E and F_C inherit CFG745's translation of the lensing excess into a mass (0.55-0.80 M*) and the X-COP missing mass under the simple
  interpolating function; F_U is bounded only from below and uncertain by ~2 dex through the R_ind accounting. The E-C gap rests on the assumption that late types
  carry F = 0 and on N = 1/f_ret from the census. If either input is wrong by a factor ~19 the gap closes; the T4 and T5 conclusions do not depend on the gap size.
- T1 uses the frozen CFG782 gates (90% / 10%) and CFG317's R_ind; both are inputs, not facts. The empty window is a statement about those inputs.
- Not verified: the TDG corollary (argument only); P4 and P5 (ledger statements, not recomputed); the lensing-to-mass translations; SPARC was omitted from T1
  (it can only tighten S2).
- Trial count: 5 frozen tests (T1-T5) + 1 post-hoc sensitivity grid (25 cells, diagnostic only) + 1 argument (section 4, not computed). One control
  comparison (T5, exact vector vs up to a scalar) was fixed after the first run and is disclosed in the script; no result changed.
