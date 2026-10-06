# CFG355: tidal rule T1 with a cold-rank veto (f = T1 AND NOT rank sigma_c == 2)

Criteria: `FROZEN_CRITERIA.md` (commit 3f59dab1b, committed alone before any script). kappa = 1/2 fixed (fitted);
nu_mono; no DM particle (the cold MASS is still required). Owner decision 2026-10-06: the switch may read the cold
component. **Under the original MS1 this reader is NOT ADMISSIBLE.**

**Verdict (frozen): NO-GO.** Three tests fail: (a'), (c) and (d). Constants n = 1, because the width is not derived.
This is a scoped result, not a closure.

## Rule
- f = H_eps(l2 - tau) * V, where V = 1 - [rank sigma_c == 2] = 1 - H(e2)(1 - H(det)).
  - T1 is CFG354's rule.
  - The rank is CFG351's stream-sum rank.
- The host rank model is scored, as frozen, with CFG351's self-similar caustics (lam1 = 0.359 r_ta, lam2 = 0.232 r_ta):
  - r < lam2: rank 3;
  - lam2 < r < lam1: 3 streams, generically rank 2 (non-collinear velocities);
  - r > lam1: rank 0.

## Results
| test | result |
|---|---|
| L legality | PASS. CFG354's L1-L4 are re-run identically. Rank part: tr(s)s - s^2 = 0 and e2 = 0 on rank 1 (2.6e-16), sigma adj sigma = det I (2.1e-17), so the switch stress is zero and V is a state function (CFG351's conservation argument applies). |
| (a) linear | PASS. ON(f) ⊂ ON(T1), with ON = 0; FRW is rank 0. |
| (a') A1: CFG353 cells, virialised rank map | PASS. The cylinder-core false ON (T1 0.04 / 0.111) drops to **0**: T1 fires only inside the core, which is rank 2. Planes are 0. |
| (a') A2: CFG351's separable Zel'dovich field, 96^3, FFT tide | **FAIL.** False ON (ON but not turned around in all three axes) is 0.9-3.1% of the volume for D 1.0-2.2. It sits in rank-0 regions (single stream, near forming caustics) and rank-1 regions (crossed in one axis). The veto removes only the rank-2 part: T1 alone gives 0.9-4.1%. |
| (b) hosts | PASS. T1 P(ON at 30 kpc) is 1.00 on 24/24, and 30 kpc < lam2 r_ta (max ratio 0.73), so the rank there is 3. Gas compression moves neither r_ta nor the caustics, and rank is congruence-invariant, so there are 0 flips. |
| (c) edge | **FAIL.** Edge c1 (CFG354's definition: continuously ON from 30 kpc) stops at lam2 = 0.232 r_ta, because the 3-stream shell is vetoed. That gives 0/24 hosts, with offsets of 135-2061 kpc. The outermost ON radius is still the T1 edge, 0.954-0.993 r_ta (reported). |
| (d) data (harness copy, actual f(r)) | **FAIL.** Details below. |

**(d) data rows:**
- control: -9.18 / -9.30.
- T1 sharp: reproduces CFG354 exactly (diff 0).
- T1 smeared (ramp of full width 2 x 0.0158 r_ta, the gap CFG354 left open): -10.47 / -11.14 and -9.78 / -10.39. PASS.
- **COMBINED** (smeared edge plus the shell veto): **+51.5 / +52.4 and +52.2 / +53.1. FAIL.** SPARC and growth pass.
- Reported:
  - smear x3: -10.44 / -11.08;
  - with filament-fed vetoes at beta 0.1 / 0.2: +53.5 and +60.2.

## Host volume vetoed (A5, reported)
- The generic shell is 3.37% of the r_ta volume and 12.7% of an isothermal phantom inside r_ta. That phantom loss is
  what costs KiDS about +62 relative to T1.
- Three feeding filaments of core radius beta r_ta (rank 2 outside lam1) add 1.4% / 5.8% / 13.0% of the volume and
  1.3% / 5.4% / 12.1% of the phantom, for beta = 0.1 / 0.2 / 0.3.
- Inside lam1 the filament's streams add to the host's, so the rank is 3 and the region stays ON.

## Filament tips and transients (reported)
- Uniform Ferrers ellipsoids are homogeneous, so the whole body has one rank:
  - crossed in 2 axes: vetoed, 0;
  - pre-crossing: T1's 100%.
- Cylindrical top-hat (EdS):
  - 2D turnaround at delta_lin 0.832 (delta 2.50);
  - delta reaches 2 tau = 3.03 at delta_lin 0.888;
  - crossing at 1.467.
  So there is a rank-0, T1-ON window of d ln a = 0.50 (53% of the age at crossing) that the veto cannot see.
- In A2 the tips (the proto-knot ends of the filament) are where TA3 and rank 2 coincide. The veto switches those
  OFF: 0.02-0.16% of the box is "false OFF".

## Width
- Not derived: n = 1, with eps_min = 0.0768 (smearing <= 1.58% r_ta), as in CFG354.
- Candidate W0, eps = l1 - l2 (the tidal split):
  - It satisfies eps >= c_d Delta/6 at 959 of 960 sampled edge points (median ratio 153, min 0.73).
  - But l1 = l2 exactly at isolated points on every tidally perturbed edge. Poincare-Hopf: a line field on S^2 must
    have singularities. The direction scan finds 4 near-degenerate points with min split 1.2e-3 |t_ext|.
  - Near those points eps -> 0 while the in-plane c_d does not. So W0 fails the pointwise bound.
- a0 gives only per-system lengths, and xi has no fixed value in the record, so neither fixes a dimensionless width.

## Reported variants (not scored)
- R1 (exactly radial orbits, 3-stream rank 1) and R2 (phase-mixed or substructured halo, rank 3 inside lam1) have no
  host hole. (c) and (d) then pass, as the T1-smeared rows show. Only (a') A2 fails, so these would be PARTIAL (n = 1).
- They improve on T1 alone in one respect: filament cores are fixed. Rank-0 and rank-1 false ON remain.

## Ownership / UFD (brief)
- Class E (GCs, wide binaries) sit in the host's full-rank interior, so they are ON. The ownership rule (CFG333 R2) is
  still needed, unchanged.
- Class A dwarfs and CFG344's UFD clumps are full rank, so they are ON. This is consistent.

## Controls
- K0: with no veto, CFG354's T1 numbers are reproduced (a, a', hosts, width, lens edges; diff 0).
- K1: ideal filament core vetoed.
- K2: isothermal halo ON to its edge (0.9998 r_ta).
- K3: planes OFF at any rank.
- MUTATE (veto rank 3), rc 1 for both scripts:
  - main: (b) ON 0/24;
  - harness: KiDS +929 / +971 and SPARC A3 0.

## Lean
`CFG355_veto_certificates.lean`: 19 theorems, no sorry, standard axioms only, rc 0 (`.out`). They cover:
- middle eigenvalue of the sphere, cylinder and plane triples;
- ON for a rank-3 or rank-0 sphere;
- OFF for a rank-2 cylinder, a plane at any rank, and the rank-2 shell;
- ON(f) ⊂ ON(T1), and the indicator bound;
- MUTATE interior OFF;
- three-stream dependence (rank <= 2);
- the rank-1 stress identity and minor;
- the sigma adj sigma diagonal and off-diagonal entries;
- the width bound V_b/V_c^2 <= 1, and eps_min > 0;
- the shell share > 3% (volume) and > 12% (isothermal phantom).

## Run
```
python3 campaign_fresh_gravity/CFG355_tidal_plus_rank_switch/cfg355_tidal_rank_switch.py > campaign_fresh_gravity/CFG355_tidal_plus_rank_switch/cfg355_tidal_rank_switch.out   # rc 0, ~31 s
python3 campaign_fresh_gravity/CFG355_tidal_plus_rank_switch/cfg355_edge_harness.py > campaign_fresh_gravity/CFG355_tidal_plus_rank_switch/cfg355_edge_harness.out 2>/dev/null   # after the main script, ~8 s
CFG355_MUTATE=1 python3 campaign_fresh_gravity/CFG355_tidal_plus_rank_switch/cfg355_tidal_rank_switch.py > campaign_fresh_gravity/CFG355_tidal_plus_rank_switch/cfg355_tidal_rank_switch_MUTATE.out   # rc 1
CFG355_MUTATE=1 python3 campaign_fresh_gravity/CFG355_tidal_plus_rank_switch/cfg355_edge_harness.py > campaign_fresh_gravity/CFG355_tidal_plus_rank_switch/cfg355_edge_harness_MUTATE.out 2>/dev/null   # rc 1
cd fable_independent_2026/lean_2026 && lake env lean <repo>/campaign_fresh_gravity/CFG355_tidal_plus_rank_switch/CFG355_veto_certificates.lean
```

**Scope:**
- The spherical self-similar model sets the rank shells. Its 3-stream shell is the scored assumption: it is what CFG351
  used.
- ZA after shell crossing is CFG351's own idealisation.
- The A2 ground truth is local ZA turnaround (D A_i cos q_i >= 1/2).
- The filament-fed geometry is a parameterised estimate.
