# CFG918: sol61 roadmap gate 1, outer-envelope energy and angular-momentum receiver capacity (Draco, Sextans, Fornax, Leo I)

**Result in one paragraph.**
- **A bound envelope fails in three places.** A finite outer envelope that stays bound cannot take up the energy a forming
  core must shed in these cases:
  - Sextans at catalogue σ: **CAPACITY EXCLUDED** in both initial geometries, on both footings;
  - Draco, and Sextans in both mass branches, when the cold stock starts at the record's catchment scale: **EXCLUDED**;
  - the stars cannot make up any of these shortfalls.
- **Escape removes the energy obstruction.** If part of the envelope may leave the dwarf's patch:
  - capacity is not the obstruction for any admissible initial spin in any of the four dwarfs (**CAPACITY ALLOWED**);
  - the one exception is Sextans at catalogue σ from a compact patch, which passes only for spins below a critical value
    (**INDETERMINATE**: in the worst case λ_c ≤ 0.37, Peebles λ_P ≈ 0.11–0.15).
- **Fornax** is ALLOWED everywhere.
- **What it means.** In the escape cases, the non-core stock has to be ejected fast: Sextans needs about 80–90 km/s. Making
  that fast ejection happen is the open problem (gate 2).
- **Scope.** Every ALLOWED is necessary feasibility only, NOT formation.

The criteria (`FROZEN_CRITERIA.md`) were committed alone, before any script or number, in **d74df7476**. Amendment **A1**
(POST HOC, three reported-only diagnostics, no class weight) was committed alone in **8c450e4d1**, before it was run.
κ = ½ is FITTED. The footings are scored separately and never pooled; the B0 and B1 mass branches are never pooled. Only raw
data and framework-native inputs are used: no HMcode, BAHAMAS, ΛCDM mass function or ΛCDM spin distribution. The cold
energy's mass is required and no dark-matter species is added. Not "theory closed", and nothing here says the data favour
the framework.

## Runs (one core, `nice -n 10`, OMP_NUM_THREADS=1, one process at a time; nothing downloaded; no PDE)

| stage | command | output | exit | wall | peak RSS |
|---|---|---|---|---|---|
| K | `python3 cfg918.py K` | `cfg918_K.out` | 0 | 0.7 s | 0.21 GB |
| MUTATE-1 | `CFG918_MUTATE=1 python3 cfg918.py` | `cfg918_MUTATE1.out`, `cfg918_results_MUTATE1.json` | 0 (bites) | ~60 s | 0.47 GB |
| MUTATE-2 | `CFG918_MUTATE=2 python3 cfg918.py` | `cfg918_MUTATE2.out`, `cfg918_results_MUTATE2.json` | 0 (bites) | ~47 s | 0.47 GB |
| main | `python3 cfg918.py` | `cfg918.out`, `cfg918_results.json` | 0 | 80 s | 0.46 GB |
| refinement | `python3 cfg918.py R` | `cfg918_REFINE.out`, `cfg918_results_REFINE.json` | 0 | 356 s | 0.61 GB |

Each JSON records the script's sha256 and the input files' sha256.

## Question and model (details in FROZEN_CRITERIA.md)

The roadmap's necessary bound is |J_req|² ≤ 2 I_out K_out ≤ 2 M_out R_max² K_available, with K_available taken from one
conserved energy ledger. It is applied to the four dwarfs with one common model.

**Gravity and the ledger.**
- All mass gravitates in the Newtonian way; cold self-gravity is class A (CFG888). This is the convention behind
  M_need = 3Rσ²/G.
- Everything is spherical. Stars (Plummer) and the settled tethered cold mass s M★ form a static external potential.
- The conserved ledger is the cold sector: E = K + W_cc + W_c,ext. J is conserved, and there is no external torque or work.

**Record inputs (CFG853 convention; K1 reproduces the roadmap table).**
- Mass branches: **B0**, catalogue σ; **B1**, σ × 10^{δ/2} from CFG861. B1 is the conditional binary shift applied
  globally, a sensitivity rather than an observation.
- Initial cold patch: the whole remaining stock M_rem, with ρ ∝ r⁻². Two geometries:
  - **G1**: on [R, r_ta], the record's catchment (CFG822);
  - **G2**: on [R, 5R], the handoff's compact cloud.
- Initial motion: coherent rotation with a fraction λ_c ∈ [0, 1] of the circular speed, plus random motion. The initial
  kinetic energy runs from the rotation alone (φ_K = 0, a turnaround start) up to the virial value (φ_K = 1).
- **λ_c has no defensible lower bound above 0.** The action does not predict the initial spin (gate 3 is open), so λ_c is
  bracketed, never fitted.

**Final state.**
- The core is M_x inside R. Three core states form a bracket:
  - **S**: thin shell at R. It is the least bound, and it may keep J up to M_x R V_c(R) (the kinematic limit for material
    confined to R).
  - **U**: uniform sphere, J = 0.
  - **C**: CFG870 cored shape with r_c = 104 pc, pressure supported, J = 0.
- The receiver is all the remaining stock, M_out = (1 − F) M_rem.
- The most favourable admissible receiver is the maximum over a two-component family:
  - a circular shell A at r1;
  - a tangential component B at r2, whose kinetic energy closes the ledger.
- Both components stay outside R (pericentre ≥ R).
- **RB (bound envelope)**: B's apocentre is ≤ R_max.
- **RE (escape permitted)**: B may leave R_max after receiving J.
- R_max:
  - G1: r_ta;
  - G2: {5R, r_ta}. r_ta is the most favourable and presumes the transfer happened before infall.

**Classes.** There are 64 graded cells (dwarf × branch × footing × geometry × receiver branch), each judged over the bracket
grid (λ_c in steps of 0.01, φ_K ∈ {0, ½, 1}, core ∈ {S, U, C}, R_max).
- **EXCLUDED**: no combination passes at any λ_c. Equivalently, the most favourable receiver fails at λ_c = 0. This audit is
  run first.
- **ALLOWED**: every combination passes at every λ_c.
- **INDETERMINATE**: anything else.

## Input ledger (units: M☉, pc, km/s; origins in brackets)

M★ = Υ_V 10^{0.4(4.83 − M_V)}, with LVD M_V and Υ_V from CFG827 (SFH). Sextans takes Υ = 2 (assumed, as in the handoff).
R = 4a/3 with a from LVD. σ comes from CFG824 or LVD; B1 applies CFG861's δ. The settled cap s comes from the law at each
footing. M_rem = (53.64 − s) M★ (53.64 = 5.364/0.1, an input). M_x = 3Rσ²/G − (p + s) M★. r_ta comes from CFG822.

| dwarf | M★ | R | s (can / alt) | σ B0 / B1 | M_rem (can) | M_x B0 / B1 (can) | F B0 / B1 (can) | M_out B0 (can) | r_ta |
|---|---|---|---|---|---|---|---|---|---|
| Draco | 5.743e5 | 257.6 | 5.364 / 5.364 (capped) | 9.55 / 9.207 | 2.77236e7 | 1.301e7 / 1.186e7 | .469303 / .427664 | 1.471e7 | 26 342 |
| Sextans | 5.261e5 | 647.9 | 5.364 / 5.364 (capped) | 7.90 / 6.566 | 2.53958e7 | 2.510e7 / 1.639e7 | .988540 / .645287 | 2.910e5 | 25 156 |
| Fornax | 1.980e7 | 927.1 | 3.616 / 3.999 | 12.10 / 12.016 | 9.90289e8 | 1.294e7 / 1.163e7 | .0130695 / .0117393 | 9.773e8 | 105 514 |
| Leo I | 3.699e6 | 305.5 | 2.700 / 2.991 | 9.29 / 9.288 | 1.88437e8 | 6.504e6 / 6.496e6 | .0345131 / .0344714 | 1.819e8 | 65 160 |

On the alt footing, M_x is smaller for Fornax (B0 5.36e6, F .005456) and Leo I (B0 5.43e6, F .028957), because s is
larger there. Draco and Sextans are identical on both footings, because s is capped at 5.364.

## Classes

**The classes are identical on the two footings.** In the table, each entry is the class followed by (λ_crit,MF /
λ_crit,all); "-" means no passing λ_c.

| B0 (catalogue σ) | G1 RB | G1 RE | G2 RB | G2 RE |
|---|---|---|---|---|
| Draco | **EXCLUDED** (- / -) | ALLOWED (1 / 1) | INDET (1.00 / -) | ALLOWED (1 / 1) |
| Sextans | **EXCLUDED** (- / -) | ALLOWED (1 / 1) | **EXCLUDED** (- / -) | INDET (1.00 / 0.37) |
| Fornax | ALLOWED (1 / 1) | ALLOWED (1 / 1) | ALLOWED (1 / 1) | ALLOWED (1 / 1) |
| Leo I | INDET (1.00 / -) | ALLOWED (1 / 1) | ALLOWED (1 / 1) | ALLOWED (1 / 1) |

| B1 (binary shift, sensitivity) | G1 RB | G1 RE | G2 RB | G2 RE |
|---|---|---|---|---|
| Draco | **EXCLUDED** (- / -) | ALLOWED (1 / 1) | INDET (1.00 / -) | ALLOWED (1 / 1) |
| Sextans | **EXCLUDED** (- / -) | ALLOWED (1 / 1) | INDET (0.86 / -) | ALLOWED (1 / 1) |
| Fornax | ALLOWED (1 / 1) | ALLOWED (1 / 1) | ALLOWED (1 / 1) | ALLOWED (1 / 1) |
| Leo I | INDET (1.00 / -) | ALLOWED (1 / 1) | ALLOWED (1 / 1) | ALLOWED (1 / 1) |

**Summary across the two geometries (both footings).**
- Bound envelope (RB):
  - Sextans B0: **CAPACITY EXCLUDED**;
  - Fornax: ALLOWED (both branches);
  - Draco, Leo I and Sextans B1: INDETERMINATE (the initial density field is not fixed; G1 is EXCLUDED for Draco and
    Sextans).
- Escape permitted (RE): ALLOWED for every dwarf and branch except Sextans B0, which is INDETERMINATE.

**Four-dwarf line (one common model).**
- RB in G1: BROKEN in both branches (Draco and Sextans are EXCLUDED).
- RB in G2: BROKEN for B0 (Sextans); B1 shows no capacity obstruction.
- RE: no capacity obstruction in any branch or geometry.

**What decides the INDETERMINATE cells** (from `lam_crit_by_combo` in the JSON):
- **Draco G2 RB.**
  - It fails at λ_c = 0 for a virial start (φ_K = 1), unless the core is the thin shell and R_max = r_ta. It also fails
    when φ_K = ½ is combined with a pressure-supported core (U or C) and R_max = 5R.
  - It passes every spin in three cases: the thin-shell core at R_max = r_ta (any start); the thin shell at 5R from a cold
    start; and U at r_ta from a cold start.
  - With the record's cored core and a cold start: λ_crit = 0.36 at R_max = 5R and 0.88 at r_ta.
- **Leo I G1 RB.** It fails only for a virial start with a pressure-supported core (U or C). From a cold start with the
  cored core, λ_crit = 0.95.
- **Sextans B1 G2 RB.**
  - Passes in only two situations:
    - from a cold start, with the thin-shell core (λ_crit 0.55 at 5R, 0.86 at r_ta) or with U at r_ta (λ_crit 0.21);
    - from φ_K = ½, with the thin shell at r_ta (λ_c ≤ 0.04).
  - The record's cored core fails in every combination. PH3 below makes this cell EXCLUDED.
- **Sextans B0 G2 RE.** With R_max = 5R and a pressure-supported core, the escaping 1.15% receiver carries the patch's J only
  up to λ_c = 0.37–0.57. Every other combination passes at every spin.

## Energy ledger (canonical, B0; units M☉ (km/s)²)

Columns:
- E_init: the cold-sector energy of the whole patch. "cold" is λ_c = 0 with φ_K = 0; "virial" is φ_K = 1.
- E_core,f: the core's final energy for each core state.
- RB cap: the largest final energy the core plus a bound envelope can hold, using the most favourable core and R_max.
- Shortfall: E_init(cold) − RB cap. A positive value means a bound envelope cannot absorb the release.
- Stars: the permissive heating tolerance p M★ · 3σ² ln 10 (CFG853 T1), shown to judge whether the stars could absorb the
  shortfall.

| dwarf, geom | E_init cold | E_init virial | E_core,f S / U / C | RB cap | shortfall | stars |
|---|---|---|---|---|---|---|
| Draco G1 | −1.98e8 | −9.93e7 | −1.11e9 / −1.50e9 / −1.89e9 | −1.14e9 | **+9.4e8** | 1.85e8 |
| Draco G2 | −2.59e9 | −1.30e9 | same | −1.14e9 | −1.45e9 | 1.85e8 |
| Sextans G1 | −1.57e8 | −7.85e7 | −1.33e9 / −1.71e9 / −2.48e9 | −1.33e9 | **+1.17e9** | 1.16e8 |
| Sextans G2 | −8.65e8 | −4.34e8 | same | −1.33e9 | **+4.65e8** | 1.16e8 |
| Fornax G1 | −5.62e10 | −2.82e10 | −2.99e9 / −4.68e9 / −7.24e9 | −1.48e10 | −4.14e10 | 1.03e10 |
| Fornax G2 | −8.46e11 | −4.25e11 | same | −1.48e10 | −8.32e11 | 1.03e10 |
| Leo I G1 | −3.21e9 | −1.61e9 | −7.91e8 / −1.19e9 / −1.57e9 | −1.46e9 | −1.75e9 | 1.13e9 |
| Leo I G2 | −8.91e10 | −4.48e10 | same | −1.46e9 | −8.76e10 | 1.13e9 |

Reading:
- **G1 (catchment scale).** In Draco and Sextans the central core, even as the least-bound shell, is more bound than the
  entire initial patch: about 5.6× in Draco and 8.5× in Sextans.
- **Sextans in G2.** Even the compact patch at turnaround holds less binding than the core needs.
- **The bound envelope.** It can absorb at most the rise to its maximal bound energy at R_max, which is nearly zero at
  large R_max. Sextans's envelope is only 2.9e5 M☉.
- **The stars.** Their tolerance is 4–10× smaller than each positive shortfall, so they are no rescue.
- **B1 Sextans.** The shortfall is +4.93e8 in G1, so it stays EXCLUDED there; in G2 it is −2.15e8, so energy is feasible and
  angular momentum decides.

## Angular-momentum and mass ledger (canonical, B0; J in M☉ pc km/s)

Columns:
- J_1: the whole patch's angular momentum at λ_c = 1. J_init = λ_c J_1.
- J_keep: the most the thin-shell core can retain, M_x R V_c(R).
- λ_P(λ_c = 1): the Peebles spin at λ_c = 1 (cold / virial start).
- Representative optimum: λ_c = 1, φ_K = 1, core S, R_max = r_ta, in the RE branch. It lists the bound envelope (A), the
  component B and whether B leaves R_max.

| dwarf, geom | J_1 | J_keep | λ_P(λ_c = 1) | RE optimum: J_req / J_cap | mass ledger at that optimum: core / A (bound, at r1) / B (at r_ta) |
|---|---|---|---|---|---|
| Draco G1 | 5.83e11 | 4.31e10 | 0.385 / 0.334 | 5.40e11 / 5.02e12 | 1.30e7 / 4.66e6 at 258 pc / 1.01e7, leaves, v ≈ 19 km/s |
| Draco G2 | 1.41e11 | 4.31e10 | 0.336 / 0.291 | 9.75e10 / 3.42e12 | 1.30e7 / 8.34e6 at 258 pc / 6.38e6, leaves |
| Sextans G1 | 5.04e11 | 1.66e11 | 0.369 / 0.319 | 3.38e11 / 6.79e11 | 2.51e7 / 0 / 2.91e5, leaves, v ≈ 93 km/s |
| Sextans G2 | 1.95e11 | 1.66e11 | 0.336 / 0.291 | 2.97e10 / 5.75e11 | 2.51e7 / 0 / 2.91e5, leaves, v ≈ 78 km/s |
| Fornax G1 | 2.41e14 | 2.43e11 | 0.352 / 0.305 | 2.41e14 / 2.19e15 | 1.29e7 / 6.19e8 at 927 pc / 3.58e8, leaves |
| Fornax G2 | 5.51e13 | 2.43e11 | 0.312 / 0.270 | 5.48e13 / 1.50e15 | 1.29e7 / 7.66e8 at 927 pc / 2.12e8, leaves |
| Leo I G1 | 1.55e13 | 2.90e10 | 0.341 / 0.296 | 1.54e13 / 1.91e14 | 6.50e6 / 1.15e8 at 305 pc / 6.67e7, leaves |
| Leo I G2 | 2.58e12 | 2.90e10 | 0.300 / 0.260 | 2.55e12 / 1.29e14 | 6.50e6 / 1.39e8 at 305 pc / 4.25e7, leaves |

The bound-envelope (RB) optimum at the same corner has no energy-feasible configuration for Draco G1 and Sextans G1/G2. Its
J_req / J_cap values in the other cells:
- Draco G2: 9.75e10 / 6.43e11 (B 1.32e7 bound at 22.1 kpc);
- Fornax G1: 2.41e14 / 4.85e14;
- Fornax G2: 5.48e13 / 2.41e14;
- Leo I G1: 1.54e13 / 3.17e13;
- Leo I G2: 2.55e12 / 1.62e13.

The roadmap's Cauchy–Schwarz form sqrt(2 M_out R_max² K) is printed for every optimum in `cfg918.out`, and K3c checks it
for all 68 793 optima.

The energy-optimal RE configurations often park a large bound envelope just outside R (Leo I: 1.15e8 M☉ at 305 pc).
Amendment A1 PH1 shows that the classes do not depend on this.

## Controls (all PASS; `cfg918_K.out`, repeated at the head of every output)

- **K1.** The roadmap table is reproduced: M_rem, F_B0 and F_B1 for the four dwarfs (12 numbers), each within half a unit of
  the last printed digit, plus M_rem and F against CFG853's JSON to 1e-9.
- **K2.** The roadmap's receiver examples M_out/M ≥ j²/α (R_i/R_out)² are reproduced to 1e-12 for all 9 (j, α) pairs of the
  sol61 `receipt.json`, including .0025/.01/.04 at α = 1.
- **K3.** Cauchy–Schwarz checks:
  - (a) a coplanar ring has J² = 2IK (ratio 1 at printed precision; tolerance 1e-12);
  - (b) random isotropic velocities give J²/(2IK) = 4.9e-6 < 1;
  - (c) every one of the 68 793 frozen-run optima satisfies J_cap² ≤ 2 M_out R_max² K. The maximum ratio is 1.000000:
    the optimum saturates the roadmap bound when all receiver mass sits at R_max.
- **K4.** Analytic energetics, all within 1e-6:
  - uniform sphere +1.5e-12;
  - thin shell −6.8e-9;
  - ρ ∝ r⁻² shell +6.7e-16;
  - Plummer sphere −2.2e-16;
  - the patch's external-potential integral, analytic against numeric, at worst 5.6e-16.
- **K5.** The CE-FM-089 Sextans example is reproduced: release 6.368e46 J (6.37e46 printed) and escape speed 469.03 km/s
  (469 printed).
- **K6.** Sextans 1 − F = .011460 (B0) and .354713 (B1), against the roadmap's .01146 and .35471.
- **K7.** Ledger closure: recomputing E_fin independently (discrete-shell core with Richardson extrapolation, plus explicit
  pair sums) matches E_init to at most 2.3e-11 relative over all 68 793 optima (the tolerance is 1e-9).

## MUTATE (both arms bite; exit 0)

- **MUT-1, core binding removed.** The core is placed at r_F, the outer edge of its own initial stock. 24 of the 64 classes
  change:
  - Draco G1 RB (both branches) and Sextans B1 G1 RB go from EXCLUDED to INDETERMINATE;
  - Leo I G1 RB becomes ALLOWED;
  - Draco RE (G1, G2), Sextans B0 G1 RE and Sextans B1 RE (G1, G2) go from ALLOWED to INDETERMINATE, because a less-bound
    core releases less energy to the escaper.
  - Sextans B0 RB stays EXCLUDED. A virialised core that has not contracted needs energy, and the 2.9e5 M☉ envelope cannot
    supply it.
- **MUT-2, starved receiver.** The receiver is 0.01 M_out; the rest leaves at zero energy, which costs its binding. 44 of
  the 64 classes change:
  - all Fornax cells, Leo I G2 (RB and RE) and Draco B0 G2 RB become EXCLUDED, because the ledger can no longer be closed;
  - Draco RE, Sextans RE (except B0 G2, which was already INDETERMINATE) and Leo I G1 RE go from ALLOWED to INDETERMINATE.

So the statistic responds to both the core's binding and the receiver's mass.

## Amendment A1 (POST HOC, reported only, no class weight)

- **PH1, receiver restricted to r ≥ 2R** (no envelope crowding the aperture edge). **0 of 64 classes change.** The ALLOWED
  cells for Fornax and Leo I do not need envelope mass parked just outside R.
- **PH2, Peebles spin at the critical points.**
  - λ_c = 1 corresponds to λ_P ≈ 0.26–0.39, depending on dwarf, geometry and start.
  - Sextans B0 G2 RE's worst-case λ_crit,all = 0.37 is λ_P = 0.149 (cold start) or 0.108 (virial start).
  - Sextans B1 G2 RB's λ_crit,MF = 0.86 is λ_P = 0.307 (cold start).
  - These are orientation only. No spin distribution is used, and the framework does not predict the initial spin.
- **PH3, record cored core only** (dropping the thin-shell and uniform limits). **2 of 64 classes change**: Sextans B1 G2 RB
  goes from INDETERMINATE to **EXCLUDED** on both footings. All other classes are unchanged.

## Grid refinement (r 160 × x 120 instead of 80 × 60; reported, the frozen-grid class stands)

**0 of 64 classes change, and no λ_crit,MF or λ_crit,all value moves.** The passing λ_c sets are contiguous from 0 in every cell, so there are no isolated passing islands.

## What is established

1. **A purely bound finite envelope is excluded for Sextans at catalogue σ** in both initial geometries and on both
   footings, at the most favourable admissible corner:
   - a cold (turnaround) start, zero spin, the least-bound core, R_max = r_ta, and all non-core stock as the receiver;
   - the shortfall is 4.7e8 M☉ (km/s)² (G2) to 1.2e9 (G1);
   - the stars' permissive tolerance is 1.2e8.
2. **When the stock starts at the record's catchment scale (G1), a bound envelope is excluded for Draco and for Sextans in
   both mass branches.** The core is more bound than the whole initial patch.
3. **Wherever a bound envelope is excluded, the core can form only if part of the stock escapes the dwarf's patch.** With
   escape permitted, capacity passes for every admissible spin in Draco, Fornax, Leo I and Sextans B1. Sextans B0 needs
   λ_c ≤ 0.37 in its worst corner. In the Sextans RE optima the entire 1.15% non-core stock leaves at about 80–90 km/s.
4. **Fornax passes every corner in both receiver branches.** Capacity is never its obstruction; its open question is the
   opposite one (not acquiring extra mass, CFG853 T2).
5. **The one common model is BROKEN as a bound-envelope mechanism** in G1 (both branches) and in G2 for B0. It is not broken
   once escape is allowed.

## What is not established

- **No formation, transfer rate or mechanism.** ALLOWED means only that the conservation laws and the finite stock do not
  forbid it. The rate test is gate 2, which needs a declared PDE or N-body run; none was run here.
- **No production or selectivity.** The initial spin, the initial density field (G1 against G2), the initial kinetic state
  and the assembly epoch are not predicted (gate 3). Several INDETERMINATE cells turn on exactly these.
- **The RE branch assumes escapers do not return.** It does not evolve their orbits in the host. "Escaped" means it left
  R_max, not that it is unbound from the Milky Way.
- **R_max = r_ta presumes the transfer finished before infall.** The present and pericentric Jacobi radii from CFG916 are
  6.7–33 R for Draco, Fornax and Leo I (Sextans is not in CFG916). These lie above 5R, so G2's R_max = 5R is tide-safe, but
  far below r_ta (102–213 R).
- **Model limits.**
  - Spherical, static final potential, and static stars and settled cold.
  - Class-A Newtonian cold gravity. CFG888's canonical-action branch, in which the cold mass has no self-gravity, is not
    modelled.
  - The receiver maximum is taken over a two-component family. The test-particle linear-programming argument says two
    energy levels suffice, but with self-gravity this is the declared bound, not a proof over all distributions.
  - The thin-shell core is a kinematic limit. PH3 shows that one class depends on it.
  - No charged carrier and no radiative channel; the charge flux is n/a.
  - No external torque. A tidal torque would be a different receiver, which would need its own derivation.

## Disclosures

- **Order and reruns.**
  - The order was K, then MUTATE-1, then MUTATE-2, then main. The frozen classes were first seen in the first MUTATE-1
    output, which prints them as its baseline.
  - The script was then changed twice, with no physics change:
    1. memory: the families in the K subset are freed, and the refinement moved to its own process (mode R) to keep each
       process under 1 GB;
    2. Amendment A1's reported-only diagnostics.
  - Every stage was rerun with the final script; the classes and numbers did not change.
- **Memory.** The first K run peaked at 0.58 GB, because it kept the 24 K-subset families alive. After the fix it peaks at
  0.21 GB.
- **G1 R_max.** In G1, R_max = r_ta is both the patch edge and the most favourable radius, so G1 has one R_max value. G2 has
  two.

κ = ½ fitted; footings never pooled; cold energy mass required; not theory closed.
