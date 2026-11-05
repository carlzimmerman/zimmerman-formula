# I6_galileon: KILLED AT THE SPARC NULL on both footings. The field solve shows a disc's flat shape helps only partly: the dust stays on in 3 of 6 SPARC-like discs (all three gas-rich dwarfs, rms 0.095-0.118 dex against a 0.086 line), and the spherical reading puts 43 % of SPARC's low-g points on (line 4.6 %)

Not blind. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.
Adopts nothing. The cold sector stays retired. This lane grades where a selector would let a dust part weigh, using
baryon data only, so it did not reopen the cold sector under the owner's 11-04 lift.

Order on record: `FROZEN_CRITERIA.md` (062648e489), committed alone before any script or number. Then `galsolve.py`
(the solver) and `i6_galileon.py` → `i6.out`, `i6_results.json`; MUTATE twin `i6_MUTATE.out`, `i6_results_MUTATE.json`.

## The action graded
A cubic galileon pi (L2 + L3, r_c = c^2/a0 per footing, matter coupling beta = 1 so that pi = 2 Phi_N when linear) sits
beside v3s. The dust term is multiplied by F(s), where s = 3 sqrt3 det H / |H|^3 is the normalized determinant of pi's
spatial Hessian in the khronon frame. Phase 1 named a quintic galileon. Its field equation vanishes identically for static
fields, and L4/L5 give c_T != c, so the determinant enters only through the selector. s = 1 in FRW and at a cored centre;
s ~ 0 in a thin disc's plane; s = -0.770 around a point mass. Every system graded here sits deep inside its Vainshtein
radius (about 1 Mpc for a MW-mass galaxy), so s doesn't depend on r_c or beta there. The footings differ at the 1e-3 level.

## Results

| gate | canonical | alt |
|---|---|---|
| X-COP s (35 rows): min / s_c (5th pct) / median / max | 0.180 / **0.241** / 0.449 / 0.822 | 0.177 / **0.239** / 0.447 / 0.821 |
| **G6-SPH**, f_SP at Y 0.5 / 0.3 / 0.7 | **0.429 / 0.464 / 0.398**, DOES NOT SEPARATE | **0.429 / 0.462 / 0.399**, DOES NOT SEPARATE |
| **G6-DISC**, axisymmetric solve, models ON | **3 of 6** (DDO154, NGC3741, IC2574): **DOES NOT SWITCH OFF** | **3 of 6**, same three |
| G6-CL, X-COP-like beta model | s 0.756 / 0.716 / 0.562 / 0.343 at 0.1 / 0.2 / 0.3 / 0.5 R500, but **0.215 at 0.7 R500**: NOT ON as frozen | 0.212 at 0.7 R500: NOT ON |
| G6-Q2 | s at Saturn -0.770, dust off; pi's own force / bound: Saturn **0.37**, Mars 4.7, Earth 0.93; MW pi tidal / Hees 2.6e-8: **FAIL** (line 0.1) | Saturn 0.45, Mars 5.6: **FAIL** |
| G6-GW | PASS (CONDITIONAL: F flat near s = 1) | same |
| **lane** | **I6 KILLED AT THE SPARC NULL** | **I6 KILLED AT THE SPARC NULL** |

G6-DISC per model, N 192, rms delta over the g_b < a0 radii (line 0.0857), canonical (alt):
DDO154 0.118 (0.118) ON; NGC3741 0.113 (0.113) ON; IC2574 0.095 (0.096) ON; NGC3198 0.080 (0.081) OFF; UGC00128 0.067
(0.067) OFF; NGC2403 0.063 (0.070) OFF.

## What it means
- **Spherically, I6 is I1 again.** In the deep regime pi' ~ sqrt(M/r), so s is set by d ln M / d ln r. That is FA1's
  zeta in other units, and f_SP comes out at 0.429 against I1's 0.425.
- **The disc shape helps, but not enough.** In the plane, s stays at |s| <= 0.05 everywhere: the Hessian is planar.
  Above a gas-rich dwarf, though, the sphere around a gas disc whose mass is still growing gives s > s_c over up to half the
  shell (W up to 0.54-0.58 at small r). The dust-weighted fraction W_enc then reaches 0.25-0.46. Discs dominated by stars
  have converged mass and read OFF, though NGC3198 sits close to the line at 0.080. The failing class is the same one that
  killed I1: gas-rich discs whose baryonic mass still rises.
- **Q2 fails as frozen, but only on pi's own force.** With beta = 1, pi's deep-regime force (a0/2)(sqrt3 v_K/c) is 0.37 of
  Saturn's bound and 4.7x Mars's. Reported, not graded: the force scales as beta^1.5 and s does not depend on beta, so beta
  <= 0.37-0.42 brings Saturn to 0.1 (Mars needs beta <~ 0.08). The dust itself is off at Saturn, and the MW's pi-tidal term
  is 2.6e-8 of Hees's line.
- **GW speed.** L2 + L3 leave c_T = c. On FRW the selector term shifts the tensor kinetic coefficient by about
  Omega_d F'(1), because s is extremal at the isotropic point. GW170817 (-3e-15 < dc/c < 7e-16; Abbott et al. 2017,
  recalled, PROVISIONAL) needs F'(1) <~ 1e-15 / Omega_d. A step F satisfies that. With L4/L5 included, alpha_T would be
  O(1) on galileon backgrounds (Creminelli & Vernizzi 2017; Ezquiaga & Zumalacarregui 2017; PROVISIONAL).
- **The action.** It can be written. F depends on second derivatives of pi, so it is free of an Ostrogradsky mode only if
  F is flat on the dust's support. The label is therefore not UNDECIDED (no action).
- G6-CL misses only at 0.7 R500. That is where the frozen beta = 0.7 model steepens past X-COP's outer rows (5 % of the
  real rows sit below s_c too). This doesn't affect the kill, which comes from SPARC.

## Checks
- K0: F = 0 gives the law to 0. K1: uniform sphere s = 1; deep point mass s = -0.769800 exactly; the spherical quadratic
  satisfies the static equation to 8e-9.
- K2: the axisymmetric solver on a spherical Plummer reproduces the spherical s to 2e-4 (r 0.3-5 a, three angles, N 192).
- Ladder: W_enc changes by at most 0.0065 between N 96 and 192, and by at most 0.055 between N 48 and 192. Every ON/OFF
  call is the same at 96 and 192. Box x2: at most 0.0018. Regulator x10: at most 0.0057. Every Newton solve converged to
  |res| < 1e-9 (largest final 1e-14), in 2-7 steps.
- MUTATE (s -> -s on the galaxy side): G6-DISC goes to 6 of 6 ON and G6-SPH's f_SP moves (0.429 -> 0.420), so the gate
  bites.
- Rerun: `i6_results.json` is byte-identical across two runs.
- Compute: 569 MB peak RSS, 42 s, one thread.

**Disclosed fix before the label was written.** The first full run took X-COP radii from FA1's code, where R500 is in kpc
but was multiplied by 1e3. The clusters then came out 1000x too large and fell out of the deep regime, giving s_c -0.94 and
6 of 6 discs ON. Fixed (`r_m = r * KPC`) and rerun. Both runs read KILLED, and the numbers above are from the fixed run.
FA1's own stored `r_kpc` carries the same 1000x label error. Its zeta is a log slope, so FA1's result is unaffected.

## What is not done
- The disc models are exponential star and gas discs with frozen thicknesses and no bulge, built from SPARC Table 1. They
  are not the rotmod mass models.
- Only six galaxies were solved. A full-SPARC disc solve wasn't run, though the spherical reading covers all 175.
- The Bullet (needs a 3D nonlinear solve) and the 15 shear keys were not computed.
- F's form is open beyond monotone and step-like. The dust amount is FA1's minimum (D = 1.5), not derived.
- X22's capture wall and X57's mu-pincer and Theorem G still stand for any successor.

kappa = 1/2 FITTED; not theory closed.
