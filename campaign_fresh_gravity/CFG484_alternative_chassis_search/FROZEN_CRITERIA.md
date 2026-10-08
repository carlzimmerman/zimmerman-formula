# CFG484 FROZEN CRITERIA: search for a relativistic chassis for candidate B that passes every chassis gate

Frozen 2026-10-08, before any CFG484 script exists. Nothing below may be edited after the commit that adds this file;
corrections go in a dated section appended at the end.

Theory survey plus checks. Offline, no downloads. Read-only on every lane named here. kappa = 1/2 is FITTED. Both a0
footings (9.3603e-11 / 1.1312e-10 m/s^2) are run wherever a0 enters a number. No dark-matter particle species is
added; the cold fluid's mass is still required. Nothing here says "theory closed". Untested is not passed.

## 0. The question, and disclosure

The owner asked for "another option that actually works". CFG467 found the record's chassis (the filtered C-H/K
khronon of L340, beta = 0) in TENSION: strictly, no alpha_c passes all twelve gates (hyperbolicity and lapse
ellipticity need alpha_c > 0; strict black-hole regularity allows only alpha_c = 0). CFG484 asks whether ANY
relativistic completion ("chassis") for candidate B passes every gate of CFG467's interval table plus GW170817 and
Cassini, and what it would cost.

Candidate B (the target): a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 fitted; kernel nu(y), nu_mono the default
(kernel otherwise free); a switch that is OFF outside bound halos; a conserved cold fluid (WORKING_MODEL_SETTLED_PHANTOM
_2026-10-06.md: the law sets a target that the fluid settles into; the fluid feels ordinary gravity of all real mass).

**Not blind.** The record lanes below were read before this file was written. Expected outcome, stated now: no record
completion passes every gate; the class "gravity = GR + Lambda, MOND only in the cold-fluid sector" (the owner's
suggestion) is expected to pass the chassis gates by GR's own theorems, but to leave the fluid-sector items open, and
its Cassini status is expected to depend on whether the Sun can hold its own settled fluid. Because the outcome is
anticipated, the status rules, the row list, the new-class computations and their pass lines are fixed here.

## 1. The gate list (fixed)

Chassis gates G1-G12 are CFG467's table, at CFG467's strict readings, applied to whatever completion is scored:

| ID | gate | strict reading used here |
|---|---|---|
| G1 | strong hyperbolicity + criterion B (user decision 09-26: a global preferred time compatible with every characteristic cone, no backward signal) | full principal symbol strongly hyperbolic in the completion's own variables; a global time exists |
| G2 | lapse / instantaneous-sector ellipticity and UV positivity | every instantaneous (elliptic) sector uniquely solvable, positive in the UV |
| G3 | F2a lapse kernel (W <= 0) invertible | as CFG467 (khronon-scheme object) |
| G4 | strong coupling | cutoff >= 1e3 x LHC energy (CFG467 G4 strict) |
| G5 | negative-phantom-lobe health | no ghost / negative inertia where the law's phantom density is negative (L340 H4) |
| G6 | PPN alpha2 | \|alpha2\| <= 1.6e-9 |
| G7 | PPN alpha1 | \|alpha1\| <= 1.1e-5 (L340's row, inherited as in CFG467) |
| G8 | binary-pulsar dipole radiation | no dipole flux beyond the CFG291/CFG311 bounds |
| G9 | cosmological G / BBN | \|G_cos/G_N - 1\| <= 0.1 |
| G10 | G_N > 0 | |
| G11 | radiative stability | small couplings stable without the Pospelov-Shang hierarchy reading (CFG320 strict) |
| G12 | black-hole regularity | reading S: regular everywhere outside r = 0, including slowly moving holes (CFG318/319) |
| G13 | GW170817 | \|c_T/c - 1\| <= 7e-16 (FRIED_CHICKEN row 6 threshold; LIT, provisional) |
| G14 | Cassini and Solar System | \|gamma - 1\| <= 2.3e-5 (Cassini; LIT) AND Q2 within 2 sigma of (3 +- 3)e-27 s^-2 (CFG357's constants) AND the anomalous radial acceleration at Mars and Saturn below the per-planet ephemeris bounds 1.4e-15 / 7.0e-15 m/s^2 (as recorded in real_research/papers/MI_FIELD_THEORY_RESULTS_2026.md section 5.1, Fienga & Minazzoli 2024; LIT, provisional) |

B-carrying gates H1-H6 (a chassis that carries nothing would pass G1-G14 vacuously: GR alone does. So a completion
"works for B" only if it also carries B):

| ID | requirement |
|---|---|
| H1 | the declared law (kernel nu declared, kappa fitted) holds in the static bound-region sector |
| H2 | messenger: whatever the law needs at a point is available in the completion without a forbidden coupling |
| H3 | attractor and support: the cold fluid reaches and holds the target (deep and transition regimes) with stated microphysics, conserving its amount (CFG44's closure; CFG472/473) |
| H4 | the switch is OFF outside bound halos through a legal term (Gap 1) |
| H5 | the fluid couples to baryons only through gravity (the working model's rule) and no particle species is added |
| H6 | the a0-Lambda tie is carried (tied with kappa fitted counts as carried; derived is not required) |

## 2. Status codes and rules (fixed)

Status per (completion, gate): PASS; FAIL; NA (the gate's object does not exist in the completion, with a one-line
proof); LEN (passes only under a lenient reading that the record lists as an owner call or stated uncertainty);
COND (passes only under a stated, untested condition); UNT (untested).

Assignment rules:
- FAIL only where a committed lane, a recorded no-go (closure_map/ACTIONS_AND_NOGOS.md N1-N22) or a computation in
  this lane shows the gate fails within its scope.
- PASS only where a committed lane computes it, a computation here does, or a standard GR theorem applies; the last is
  labelled LIT (standard, not re-derived).
- Memory-only or summariser-only facts are labelled; they never upgrade a status to PASS.
- Everything else is UNT.

Classes for a completion:
- **WORKS (for B):** every G1-G14 and every H1-H6 is PASS or NA.
- **CHASSIS-CLEAN:** every G1-G14 is PASS or NA (H gates not all passed).
- **INCOMPLETE:** no FAIL, no LEN; some UNT or COND.
- **TENSION:** no FAIL; some LEN.
- **FAILS:** at least one FAIL.

Ranking (to name the top candidate): fewest FAIL, then fewest LEN, then fewest UNT+COND over G1-G14, then the same
counts over H1-H6, then fewest constants beyond kappa and Omega_c h^2. Constants are counted from the record where the
record counts them; otherwise the named constants are listed and marked "not counted on the record".

Lane verdict: **FOUND** if any completion is WORKS; **CHASSIS ONLY** if none works but at least one is CHASSIS-CLEAN;
**NONE** otherwise.

## 3. The rows (fixed before scoring)

Record completions (sources in parentheses; each row cites the lane that sets each status):
1. C-H/K chassis, strict (L340, CFG467 and its sources).
2. C-H/K at alpha_c = 0 (minimal Horava; CFG467 G1-G5, XC2).
3. C-H/K with reading W for black holes (CFG467 option 1; owner call; no new constant).
4. C-H/K plus a Horava UV sector M_* (CFG467 option 2; +1 constant; untested).
5. Candidate B's current working model on C-H/K: settling + khronon-lapse messenger (CFG373, CFG381, CFG462).
6. V0 covariant action (chk_v0_2026 CV1-CV4; DE12/DE13; MS1-MS5).
7. Derivation-chain action (FP7/FP14/XR20/XR25; closure_map row).
8. AeST v9 embedding / FC-AeST (N7).
9. FC-KH khronometric f(a) (N6).
10. Blanchet-Skordis khronon dust BS24 (BSK1, BSX1, BSX3/N8).
11. Astra CA4/CA5 common action (AS233/AS234/N22; unreviewed).
12. Astra IC28 integrable clock (closure_map row).
13. Generated phantom GP0-GP5 and the vacuum-gated L357-L361 constructions (non-relativistic; embedding = V0).
14. Dark-energy gate DE1-DE13 (the gate as a varied term, N14).
15. MOND-sector gate MS1-MS5 (non-relativistic; embedding = V0).
16. FRIED_CHICKEN frame flip (S = R[g~] + S_dark[g] + S_m[g~]; FRIED_CHICKEN.md rows 1-10 and banner).
17. GR + dark field, no MOND field (CFG2/CFG5/CFG9/CFG10/FG004, CFG43/CFG44; N20).
18. Superfluid dark matter, Berezhiani-Khoury (door 4, CFG122/CFG154).
19. Dipolar dark matter (door 3, CFG121/CFG157).
20. BIMOND (door 13, CFG232).
21. Covariant emergent gravity (door 12, CFG231).
22. Mimetic (door 10, CFG124/CFG152).
23. Nonlocal metric Deser-Woodard / RR (door 9, CFG123/CFG153).
24. Modified-inertia field theory (real_research/papers/MI_FIELD_THEORY_RESULTS_2026.md; TOE map wall 2).
25. Condensate / DBI v9 dark sector (N9) and CQ gravity (L313/L314): listed as closed families, scored only where the
    record states a gate.

New classes (not tried on the record as chassis), each with a first gate pass of the kind stated:
- **NC1: GR + Lambda chassis, MOND only in the cold-fluid sector.** Gravity is exactly GR with Lambda; baryons and the
  cold fluid couple minimally to one metric; the fluid settles, in bound regions, toward the target written as a local
  functional of its OWN 4-acceleration A (in hydrostatic/Jeans equilibrium A equals the total field, and CFG373 G1
  showed the P2 target is a local functional of the total field). Scored in its non-Lagrangian (relaxation/
  dissipative) form; its Lagrangian forms are mapped onto record classes (N1g below).
- **NC2: khronon whose alpha_c is screened to 0 in strong fields** (alpha_c a field-dependent function).
- **NC3: invertible disformal / two-time-scale redefinitions of the khronon chassis** (argument only).
- **NC5: Einstein-aether (aether not hypersurface-orthogonal)** (argument only, against criterion B).
(NC4 = row 4 above.)

## 4. Computations (fixed, with pass lines)

Controls (main run; load-bearing unless marked):
- K1: CFG467's committed JSON gives union I_strict = EMPTY, I_len = [9.6240e-14, 3.2000e-09], verdict TENSION.
- K2: CFG373's perfect square, g^2 + a_L^2 = (g_N + a_L)^2 for g = sqrt(g_N^2 + a0 g_N), a_L = a0/2 (sympy expand).
- K3: the P2 point-mass cold mass M_c = M(sqrt(1 + x^2) - 1) (CFG44 B1) from the spherical identity, <= 1e-10 rel.
- K4: the ephemeris rows: a constant a0/2 anomaly reproduces MI_FIELD_THEORY_RESULTS section 5.1's exclusion factors
  (Saturn 6686x, Mars 33429x, canonical) to <= 1%.
- K5: CFG357's script holds Q2C = SIG = 3e-27 (string read).
- K6: Bcommon's nu_mono equals nu_RAR to <= 1e-6 relative at y = 0.1, 1, 2, and max \|log10(nu_mono/nu_RAR)\| over
  y in [1e-3, 1e3] is 0.0104 +- 0.0005 at y = 14.35 +- 1 (the 09-26 user-decision numbers).
- K7: the interval parser and the classification/ranking engine on toy rows.
- K8: Schwarzschild Kretschmann scalar = 48 G^2 M^2/(c^4 r^6) from the metric (sympy), finite for r > 0.

NC1 first gate pass:
- N1a (G12): Kerr/Schwarzschild are regular outside r = 0 (LIT, standard), with K8 as the computed instance; the
  fluid is a test matter field near holes.
- N1b (H2, messenger): (i) sympy: for ds^2 = -(1 + 2 Phi) dt^2 + (1 - 2 Phi) dx^2 the static congruence's
  4-acceleration is grad Phi to first order; (ii) y nu(y) is strictly increasing on y in [1e-8, 1e8] for nu_mono and
  P2, so the inversion g_tot -> g_N exists and the target is a local functional of \|A\| for both kernels. PASS line:
  both hold.
- N1c (reported, not a gate): EP blindness. A uniform external field leaves the fluid's own 4-acceleration field in
  the freely falling system frame unchanged, so NC1's target carries no external-field effect; for comparison the
  algebraic law's field at r = r_M changes by the printed factor at g_e = 0.01, 0.1, 1 a0.
- N1d (G14), three readings, both footings:
  - R1: Sun embedded in the Milky Way's settled fluid; settling conserves phase-space density for embedded systems.
    Host fluid at R0 = 8.2 kpc from the P2 point-mass law with M_b = 6e10 Msun (declared; x3 reported); sigma_host =
    V_c(R0)/sqrt 2; coarse-grained Maxwellian f_max = rho_host / ((2 pi)^(3/2) sigma^3). Liouville cap on the
    Sun-bound density rho_cap(r) = f_max (4 pi/3) v_esc(r)^3, anomaly G M_cap(<r)/r^2 at Mars and Saturn: PASS line
    <= 0.1 x the bound. MW-fluid tide \|4 pi G rho_c - 3 G M_c(<R0)/R0^3\| <= 9e-27 s^-2; MW-fluid monopole
    (4 pi/3) G rho_c r at Saturn <= 0.1 x 7.0e-15; gamma - 1 = 0 (GR) plus the fluid contamination
    rho_c (4 pi/3)(1 AU)^3 / M_sun <= 2.3e-5.
  - R2: the Sun owns its own settled target with nu_mono: anomaly (nu(y) - 1) g_N at Mars and Saturn.
  - R3: same with P2.
  - Status rule fixed now: G14 = PASS if R1 passes and the settling microphysics is shown phase-space conserving for
    embedded systems; COND if R1 passes but that is not shown (R2/R3 then decide only if the Sun can hold fluid);
    FAIL if R1 fails.
- N1e (G6/G7): fluid contamination of preferred-frame effects bounded by rho_c (4 pi/3)(1 AU)^3 / M_sun; PASS line
  <= 1e-3 x the strict alpha2 bound.
- N1f (fluid-sector analog of G5, reported as an NC1 F-gate, not as G5): realisability of the target with real mass.
  Razor-thin exponential disc, QUMOND phantom density off the plane, rho_ph = -(1/4 pi G) nu'(y) grad y . g (g the
  Newtonian acceleration), plus the positive surface term (nu - 1) Sigma. (M_b, R_d) = (1e9, 1.0 kpc), (1e10,
  2.0 kpc), (1e11, 3.5 kpc); kernels P2 and nu_mono; canonical (alt reported). Grid R in [0.05, 20] R_d, z in
  [0.02, 20] R_d, log-spaced; the slab z < 0.02 R_d is excluded and said so. eta = \|M_neg\| / (M_pos + M_surface).
  PASS line eta <= 0.01. Convergence: a 1.5x denser grid must move eta by <= 0.2 eta + 1e-4, else NOT CONVERGED
  (reported).
- N1g (reading, argument only): a Lagrangian term f(rho_c, A) for an irrotational cold fluid is either
  foliation-invariant (then it is a khronon dust: BS24 class, N8 closes it for any K) or shift-symmetric with second
  derivatives of the phase (Ostrogradsky unless degenerate; FRIED_CHICKEN banner's dark_sector_honesty no-go for the
  g_b construction; degeneracy untested). So NC1 is scored only in its non-Lagrangian relaxation form; covariant
  relaxation-time hydrodynamics/kinetics (Anderson-Witting type; Israel-Stewart/BDNK causality) is cited as LIT for
  the form's existence, not for B's content.

NC2 first gate pass:
- N2: read CFG467's strict sets for G1 and G12. A field-dependent alpha_c(x) must satisfy G1 pointwise (frozen-
  coefficient principal symbol, CFG292's scope) and G12 at the universal horizon. PASS iff G1_strict intersect
  G12_strict is non-empty. If empty: NC2 FAILS strictly; with G12 lenient it reduces to CFG467's reading W plus >= 1
  screening constant, i.e. dominated by row 3.

NC3, NC5: argument rows only (status UNT or FAIL with the argument printed; no number).

## 5. MUTATE (fixed)

`CFG484_MUTATE=1`: the harness is applied to known-failing completions fed as the candidate under test, each of which
must come out FAILS with the recorded failing gate among its FAIL gates:
- M1: C-H/K strict (row 1) must fail at G12 (CFG467).
- M2: AeST v9 (row 8) must fail at G7 (N7).
- M3: superfluid BK (row 18) must fail at G14 (CFG122 G5.4).
- M4: NC1 with G14 scored by reading R2 (Sun owns its target) must fail at G14 (computed here).
The MUTATE run's final check "the candidate under test WORKS" must fail, so the run exits 1 as required; each
"fails at the recorded gate" check is printed. If any of M1-M4 came out WORKS or CHASSIS-CLEAN, or failed at a
different gate only, the harness does not bite and that is reported as a control failure (kept).

## 6. Outputs

`cfg484_chassis_search.py` (+ a data module for the record table), `cfg484_chassis_search.out`,
`cfg484_results.json`, `cfg484_chassis_search_MUTATE.out`, `cfg484_results_MUTATE.json`, `README.md` (plain: the
table, the top candidate and its decisive next test). Main run exits 0 iff all load-bearing controls pass. git add
only this folder; commit locally; do not push. No names or home paths in committed files.

## 7. What this lane cannot say

It maps the record and runs first gate passes. It does not build an action for B, does not solve coupled field
equations, does not test any fluid-sector dynamics beyond the computations above, and does not say any data favour the
framework. A CHASSIS-CLEAN result is not "the theory works". kappa = 1/2 stays fitted.
