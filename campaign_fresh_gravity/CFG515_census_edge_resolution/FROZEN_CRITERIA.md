# CFG515 FROZEN CRITERIA: is the growth-vs-lensing "clash" an artefact of using the f_ret = 1 edge for real galaxies?

Committed alone, before any CFG515 script exists. kappa = 1/2 is FITTED. Footings 9.3603e-11 / 1.1312e-10 (canonical / alt),
scored separately, never pooled; a0 flat. "Cold energy" = candidate B's cold component; its MASS is still required (no particle).
On-disk data only, local compute, no downloads, nice 15, <= 4 threads. Not "theory closed"; nothing here says the data favour
the framework.

## Hypothesis (from CFG513)
The PAPER45 edge is r_edge = r_M(M_b,now) / ln(1 + f_ret f_b/(1 - f_b)): the settled phantom equals the cold share of the
ORIGINAL baryons, M_ph(<r_edge) = 5.364 M_b,now / f_ret. The PM growth runs never deplete baryons, so f_ret = 1 is the
self-consistent value THERE (CFG423/424; growth passes). Real galaxies have lost most of their baryons. CFG485/487 (KiDS,
early-type levels, SPARC alt dwarfs) and CFG513 (MW timing, satellites) scored real galaxies with f_ret = 1 and failed. Test:
score the consistent picture (real objects get the census f_ret, NOTHING fitted).

## 1. Census f_ret (fixed here, before any scoring)
- **Primary: CFG416's declared retention-mass relation `fret_of`** (CFG416 FROZEN_CRITERIA, 10-07; engine `cfg416_pm.py`):
  f_ret = 0.10 for log M_ta < 12.5 (M_ta in Msun/h), linear in log M_ta to 0.55 at 13.5, then +0.30 per dex, capped at 0.90.
  M_ta is tied to the object's present baryons exactly as CFG416 defines it, M_b,now = f_ret f_b M_ta with f_b = 0.157 and
  h = 0.674 (CFG416's constants), solved self-consistently per object (fret_of is non-decreasing in M_ta and M_ta falls with
  f_ret, so the root is unique; brentq).
- **Bracket (reported for every test): constant f_ret = 0.07 and f_ret = 0.18**, the census spread stated in PAPER45 v1.0
  ("Retention varies (7-18% in the census)"; 0.18 = CFG365/CFG390 all collapsed phases, used by CFG513).
- The verdict of every test is decided by the PRIMARY. A test is called "bracket-robust" only if both bracket ends give the
  same pass/fail as the primary; otherwise "bracket-sensitive", stated as such.
- No f_ret is fitted anywhere. A post-hoc "f_ret needed" may be printed as a diagnostic, labelled, with no verdict weight.

## 2. Edge formula (fixed)
- Supply: M_cold = (1 - f_b)/f_b * M_b,now / f_ret, (1 - f_b)/f_b = 5.364 (f_b = 0.02237/0.14237, the engine value).
- Point-mass objects (KiDS lens groups, CFG485 stack nodes, SPARC rows, M31): r_edge = r_M / ln(1 + f_ret f_b/(1 - f_b)),
  r_M = sqrt(G M_b,now / a0), nu_mono kernel. Extended MW baryons: CFG513's `Prof` (numeric root of M_ph(<r) = M_cold).
- Phantom fully settled inside the edge (m = 1, "edge only"), frozen beyond it. Where a harness has a turnaround radius
  (KiDS / CFG503 / CFG485 stacks), the law is not ON beyond r_ta: outer radius = min(r_edge, r_ta). The MW uses CFG513's
  O-MW profile unchanged (no r_ta cap).
- Not modelled (declared): partial settling (CFG485 R5 found 9-14% of late types unsettled at a census edge), baryon
  profile changes from depletion, non-spherical effects.

## 3. Tests (both footings; primary census unless stated)
**(a) KiDS isolated lenses.** (a) passes iff (a1) AND (a2).
- (a1) CFG413 harness (CFG377 stack P, 181,477 lenses, 15 bins, 50-patch jackknife, Hartlap; free R^-0.8 two-halo
  amplitude profiled): chi2 - chi2_best(CFG413, x = 0.5: 8.948 / 9.770) <= 4 on both footings. Drop-one-bin reported.
- (a2) CFG503's frozen environment (E = halofit xi_NL x Tinker zeta beyond r_ta, leaked-satellite stripping at the Jacobi
  radius, Moster+13 primary with the Behroozi+13 difference as a rank-one covariance term; CFG503's code imported read-only),
  inner trusted bins only (R <= 0.3/h = 0.445 Mpc, 9 bins): chi2_inner9(census edge) - min over CFG503's five frozen models
  (LCDM, LAW_RTA, EDGE, V1, F_DD) of chi2_inner9 <= 4 on both footings. CFG503's G1/G3 validation gates FAILED; that label is
  carried on every (a2) number. Reported, no verdict weight: chi2_inner9 minus LAW_RTA's (does any failure belong to the edge
  or to the law itself in this environment), full 15-bin chi2.
**(b) Early-type lensing levels (CFG485 caveat 2 / R8).** CFG485's machinery (CFG95 calibration, CFG61 grid stack, released
  per-class K1 blocks, two-halo profiled per class, 6 dof), executed read-only: early types pass iff
  chi2(census edge) - chi2(B1, CFG95's law to 0.40 r_ta) <= 4 on both footings. Late types: same rule, reported only.
**(c) SPARC.** CFG346 S clauses via CFG487's copied harness: S-A3 >= 90% (|d log v| < 0.03 at R_HI) for spirals AND dwarfs,
  and rotmod RAR |d rms| < 0.005, both footings.
**(d) Milky Way.** CFG513's machinery (M_b = 6.0e10 primary with L172 shapes; M31 = 1.2e11 point mass), each object with its
  OWN census f_ret: passes iff LG timing (O-MW, with Lambda) |z| <= 3 against -109.3 +- 4.4 km/s (measurement error only, as
  CFG513) AND CFG433's V_c at 78 kpc, D = (231.9 - V)/21.4 <= 3, both footings. Reported: unbound Fritz satellites, the
  7.3e10 variant, the post-hoc f_ret the timing needs.
  DISCLOSED KNOWLEDGE: CFG513 already printed the f_ret = 0.18 cells (z = +3.1; D +2.89 / +2.52), so the upper bracket end of
  (d) is known in advance to miss the |z| <= 3 line by 0.1 sigma. The primary (CFG416 relation) has not been computed.
**(e) Cluster unsettled fraction.** u = 1 - settled(<R500)/dark(<R500), settled = min(M_ph(<R500), supply), at CFG453's
  committed medians (nu - 1, x_T15) for b = 0 and 0.3, clusters' f_ret from fret_of at the cluster M_ta: passes iff u at both
  b ends lies inside the record range [0.433, 0.628] (canonical) / [0.368, 0.584] (alt) (CFG453/CFG464). DECLARED: (e) is
  structurally blind to any f_ret <= 1 (supply >= 5.364 M_b > nu - 1 = 2.9-3.3), so its pass carries no weight beyond "the
  census edge does not empty clusters". Reported: the budget dark(<R500)/M_b <= 5.364/f_ret.

## 4. Verdict rule (primary census, no fitting)
- **CLASH DISSOLVED** iff (a), (b), (c), (d) all pass on both footings (and (e) passes; an (e) failure downgrades to PARTLY).
- **PARTLY** if at least one of (a)-(d) passes (each per both footings), but not all.
- **NOT DISSOLVED** if none of (a)-(d) passes.
- Each test's bracket robustness is stated beside it.

## 5. Growth: logical status (argued, no new PM job unless essential)
State whether f_ret = 1 in the growth sims is consistent with f_ret < 1 for real galaxies, citing CFG416 (census radius with
UNDEPLETED PM baryons: canonical 0.092, alt 0.101 at 512^3), CFG423 (f_ret = 1 pass; MUTATE f_ret = 0.01 TENSION 0.139) and
CFG424 (zero-knob 0.027/0.029). The argument must say what the total settled mass and its radial placement are in each case,
and label what is argued vs computed. If the argument cannot bound the consistent case, specify the PM run that would.

## 6. Controls (load-bearing)
- K1 closed-form point-mass edge = numeric nu_mono root of M_ph(<r) = M_cold to 1e-6 (f_ret 1, 0.18, 0.07, 0.01).
- K2 this lane's fret_of equals CFG416's (function text exec'd from cfg416_pm.py) on a grid to 1e-12; self-consistency
  residual < 1e-9 for every object.
- K3 KiDS harness: m = 1 sharp edges at x = 0.5 and 1.0 reproduce CFG413's committed chi2 within 0.01.
- K4 CFG503: re-scoring the committed own tables reproduces CFG503's committed LAW_RTA and EDGE chi2 (full and inner-9) within
  0.01.
- K5 CFG485 machinery reproduces CFG485's committed R8 B1 chi2 (2.548 / 2.865 early) within 1e-3.
- K6 SPARC harness C3 (m = 1, no edge: A3 = 100%, d rms = 0; rms0 = CFG39's).
- K7 CFG513 machinery at f_ret = 0.18 (both objects) reproduces CFG513's timing v_r (-122.8) within 0.5 km/s and D within 0.02.

## 7. MUTATE (`CFG515_MUTATE=1`, outputs `*_MUTATE.*`)
- M1: f_ret = 1 for every real object must REPRODUCE the record's failures: KiDS a1 d_vs_best +60.5 / +70.6 (CFG487
  edge_only_E1) within 0.5; CFG503 EDGE inner-9 240.9 / 240.7 within 1; early-type S 30.5 / 38.1 (CFG485 R8) within 1; SPARC
  alt dwarf A3 0.864 within 0.01; MW timing z -22.8 within 0.3. The f_ret = 1 verdict must not be DISSOLVED.
- M2: f_ret = 0.01 (unphysically depleted) must FAIL at least one of (a)-(d).
- The MUTATE run exits 1 if M1 or M2 is not detected.

## 8. Outputs
Scripts, `.out`, `_MUTATE.out`, JSON, a plain README. `git add` this folder only; commit locally; do not push.
