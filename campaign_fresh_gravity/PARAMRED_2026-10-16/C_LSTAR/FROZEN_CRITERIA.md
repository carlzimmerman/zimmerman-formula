# PARAMRED lane C (LSTAR): what is the stiffness length L*? (frozen criteria)

Written 2026-10-16, before any script of this lane was run and before any number of this lane existed. No CFG id is taken
(the orchestrator assigns ids). kappa = 1/2 is FITTED; both footings (a0 = 9.3603e-11 canonical, 1.1312e-10 alt) are never
pooled; the cold-energy mass is required; no particle species is added; nothing here says "theory closed" or that the data
favour the framework. Verdicts use raw data and framework-native quantities only.

## The object
S2 action term (gamma/2)|grad P|^2 with gamma = K L*^2 / 2, K = 4 pi G (so gamma = 2 pi G L*^2; CFG659). Point-mass reduction
(CFG691): inside the screening radius ell_gamma = L*^2 / (2 r_M), r_M = sqrt(GM/a0), the anomalous acceleration is the
constant GM/L*^2 (a0-free); outside, the deep law. Record statement under test (THEORY_CANONICAL_2026-10-14, S2):
"L* in [5.75 pc, >~ 1 kpc] (bounded, not derived)".

## Already on the record (cited, NOT re-run, not re-derived)
CFG691 (window, SPARC to the 1000 pc grid edge, K1 line error disclosed), CFG694 (G3 star halos, 0.155 allowance), CFG658
(E1 DR3 wide binaries, E3 star halos), CFG740 (sealed DR4 envelope), CFG770 (Cassini Q2 ~ L*^-3), CFG771 (saddle ~ L*^-2),
CFG772 (lab, L*-independent null), CFG774 (probe pull ~ L*^-2), CFG816 (DR4 R-statistic error model), CFG659/744/699
(P-wave signatures; identification c_P and relaxation at L* = 5.754 pc ONLY), CFG760-762 (P-wave export closed),
CFG782 (selector DEAD), CFG722/720 (merger response; L* ~ 1 kpc slow corner; CFG720 queued, unscored).
CFG642 and the 32-pi campaign are closed and are not touched.

## Part 1: constraint intersection (script `lstar_constraints.py`, one process, small text/JSON inputs only)
Every row is read from a recorded JSON (or from the recorded formula) and written to `lstar_constraints_results.json`.
Margins in the verdict come from that JSON, not from memory.
- **R1 Saturn mass gate (CFG691 G-SS).** Anomalous enclosed mass M (r/L*)^2 inside 9.54 AU < 6.7e-11 Msun. Because the
  inner pull is exactly GM/L*^2, ratio(L*) = ratio(5.754 pc) (5.754/L*)^2. Exact edge L*_Sat = 5.754 pc * sqrt(ratio at 5.754).
  Control: root of the full-profile ratio (CFG691's own g_an with the solved profile) agrees with the scaling to 1e-3.
- **R2 1-AU gate** (3.66e-14 m/s^2): same scaling, edge L*_1AU.
- **R3 Cassini Q2 (CFG770).** |Q2| ~ L*^-3 (CFG770 T2, checked on its own ladder to 1e-3): L*_Q2 = 5.75 pc * (worst |Q2|/ceiling)^(1/3).
- **R4 star halos (CFG694 G3 / CFG658 E3).** M_ph/M = (r_b/L*)^2 with r_b = 1.08 pc, <= 0.155 (local non-baryonic to baryonic ratio,
  declared external measurement of CFG694): L*_E3 = 1.08 pc / sqrt(0.155). Conditional on the 1.08 pc truncation of CFG694.
- **R5 wide binaries.** Formula of CFG740, gamma_v - 1 = (1/2)(s/L*)^2 (inner limit, S = 1 within 1e-3 at s <= 236 kAU, from
  the CFG740 JSON). A 2-sigma upper limit beta on gamma_v - 1 at separation s gives L* >= s / sqrt(2 beta). Rows: (a) the
  DR4 R-statistic error model of CFG816 (sigma_tot = sqrt(sigma_fit^2 + 0.02^2), sigma_fit = 0.019 sqrt(30000/N); control: the five
  recorded sigma_tot values to 1e-3), s = 50 kAU, beta = 2 sigma_tot; (b) the precision a null must reach to move the lower
  edge above R1; (c) the response to a DETECTION b = R - 1 (L* = s/sqrt(2b)); (d) DR3 (CFG658 E1): reported as the record
  has it (no injection at L* < 5.754 pc other than L* -> 0, which is excluded at 7.73/8.25 sigma); an indicative bound is
  labelled as such. A separation beyond the registered statistic (236 kAU) is a labelled extrapolation.
- **R6 fixed-L* sealed predictions** (CFG774, CFG771, CFG772): L*-scaling reported, kill lines mapped to L*.
- **R7 SPARC upper edge (NEW compute, only upper bound on the record's route).** CFG691's statistic, copied read-only:
  screened nu = 1 + y^-1/2 S(R/ell_gamma(M_b)), M_b = V_bar^2 R / G at each galaxy's last point, Upsilon_disk profiled on
  0.30-1.20 (step 0.01), rms line 0.110 dex. Scan L* on a 0.01-dex grid from 1 kpc to 30 kpc, both footings.
  L*_max = the largest grid L* at which the rms is <= 0.110 with every smaller scanned L* also passing.
  Reported only (no verdict weight): lines 0.105 and 0.115; the variant M_b(<R) = V_bar^2(R) R / G at each point (instead of
  the last point); the Upsilon at the edge.
  Controls: K1 the profile table reproduces CFG691 JSON; K2 rms and Upsilon at 316.2 and 1000 pc reproduce CFG691 JSON (1e-6);
  K3 rms at 7585 pc (alt) and 9549 pc (canonical) reproduce CFG760 JSON (1e-6).
  **MUTATE (negative control):** S = 1 (no stiffness). The scan must find NO edge up to 30 kpc on both footings (the edge is caused by
  the stiffness, not by the scan or the line). Exit code 1 iff it bites.
- **R8 P-sector branch conditions (reported, not constraints on the framework).** (a) CFG760 G3: L*_all for P-wave export (read
  from the JSON). (b) CFG744 N2(a) identification, c_P^2 = gamma/I = 2 pi G L*^2 rho_c with I = 1/rho_c (CFG698):
  c_P is proportional to L*, so t_relax = A s0^(3/2) ell_gamma / c_P = A r^(3/2) ell_gamma^(-1/2) / c_P scales as L*^-2 at fixed
  (M, y, r, rho_c). L*_open(case) = 5.754 pc * sqrt(t_medium(case) / 4.6 Gyr), t_medium read from the CFG744 JSON; the
  hatch needs all twelve cases. Also reported: s0 at L*_open per case (the s0^(3/2) law was fitted on s0 in [10, 80] only).
  Branch is CLOSED over the whole window iff L*_all(branch) > the SPARC edge (R7) on that footing.
- **R9 UFD / dwarfs (reported only).** Screening factor S(r_h/ell_gamma) for generic M_b and r_h = 30 pc at several L*. No UFD
  verdict: CFG259's table carries no stellar masses and S4 supplies the UFD mass independently (CFG691 says the same).

## Part 2: is L* derived from anything else? (derivation, frozen BEFORE comparison with the window)
- **D-A (theorem, dimensional analysis of the static action).** The static action contains G, a0 and one new constant gamma.
  [G] = m^3 kg^-1 s^-2, [a0] = m s^-2. Only G carries kg, so any G-free-of-kg combination has G^0, leaving a0^x with
  [a0^x] = m^x s^(-2x): a length needs x = 0 for seconds, then m^0. No length exists from {G, a0}. So the static action cannot
  fix L* from its own scales: L* is its own constant (CFG679 R1 already counts it as the one allowed new constant).
- **D-B (hierarchy).** With c and S1 (a0 = kappa c sqrt(G rho_DE), so rho_DE adds nothing beyond a0 and kappa) the only length is
  c^2/a0: **9.60e26 m = 3.11e10 pc (canonical), 7.94e26 m = 2.57e10 pc (alt)**, times a dimensionless number. Every
  dimensionless number the framework has (kappa = 1/2, Omega_c/Omega_b = 5.364, Omega_Lambda) is O(1). A tie L* = f c^2/a0 with f = O(1)
  would put L* at ~10^10 pc. Frozen rule: **NO TIE unless a framework dimensionless number of order 10^-7 to 10^-10 exists; none
  is on the record.** This is stated as a scale argument, not a search; no combination is tuned toward the window.
- **D-C (c_P tie).** c_P = sqrt(gamma / I). gamma = 2 pi G L*^2 (CFG659). For an independent light field I (hence c_P) is a second
  unfixed constant: no tie. For the identification P = -rho_c xi (I = 1/rho_c): c_P = L* sqrt(2 pi G rho_c), a real tie, tested
  in R8(b). Frozen prediction of R8(b): the L*_open ladder scales as sqrt(t_medium); the largest case is canonical (1e11, y = 0.1).
- **D-D (gap).** The vacuum (P = 0) has no mass term (critical action, CFG694 G1), so the gap is a property of a background
  (CFG760: 2|v0|/s in units of ell_gamma): L* is the unit of length of that gap, not an output of it. Frozen reading: the gap
  chain defines inequalities on L* for P-wave export (R8a), not a value.
- **D-E (capacity a0/(pi G)) and S4 selector (CFG782).** Neither contains L*; a length from a surface density needs a mass.
  Not computed (nothing to compare). CFG782 is DEAD.

## Verdict rules (frozen)
- **REDUCTION DERIVED** (Part 2) iff a relation derived from the action fixes L* from other framework quantities AND its value
  (written above before comparison) lies inside [R1 edge, R7 edge] on both footings.
- **CONSTRAINT TIGHTENED** (Part 1) iff the SPARC edge of R7 is finite (a number below 30 kpc) on both footings. It is labelled
  approximation-conditional (CFG691's point-mass screening of extended systems) and SOFT if the edge moves by more than a factor
  3 across the reported-only variants/lines. The lower edge is the larger of R1-R4; a DR4 outcome is mapped, not assumed.
- **NO REDUCTION** otherwise. If NO REDUCTION, the report states the single measurement that pins L*.
- A relation found only AFTER seeing the window would be labelled post-hoc and given no weight.

## Trial count (hypotheses tried, declared now)
8: (1) SPARC has a finite upper edge; (2) lower-edge intersection of R1-R4; (3) DR4/DR3 mapping; (4) {G, a0} gives a length;
(5) c^2/a0 hierarchy; (6) identification c_P tie; (7) P-wave export hatch (recorded, re-compared); (8) UFD/dwarf direction
(reported only). No parameter is scanned to hit a target. R8(b) and R7 scans are scales/edges, not fits.

## Controls summary
K1/K2/K3 (reproduce CFG691/CFG760 numbers), K4 (Saturn root vs scaling), K5 (CFG816 sigma_tot values), K6 (Q2 ~ L*^-3 on CFG770 ladder),
K7 (CFG740 envelope: gamma_v - 1 at 50 kAU and L* = 5.754 pc equals the JSON value to 1e-3). MUTATE (R7): S = 1 gives no edge.

## ADDENDUM (written after the runs; the text above is unchanged)
Disclosures, none of which changes a frozen rule:
1. **Compute gate.** The first run of `lstar_constraints.py` peaked at 467 MB RSS (limit 300 MB; the gate was open, 7 s, nothing else
   was running). Cause: the SPARC fit's temporaries plus the scipy.optimize import. The script was then changed to (a) drop
   scipy.optimize (plain bisection), (b) process the Upsilon columns in 7 blocks (identical arithmetic), (c) carry a max-RSS
   guard that stops at 285 MB. Rerun: 181 MB, 7.6 s; MUTATE 140 MB, 1.1 s. All reported numbers come from the rerun
   (K2/K3 reproduce CFG691/CFG760 to 1e-6, so the chunking changed nothing).
2. **Extra reported-only row.** R8(c), the exponent-free one-crossing bound (t ~ L*^-1, 13.8 Gyr, necessary only), is in the script but
   not in the frozen R8 text. It has no verdict weight. It matters for how R8(b) is read (see README).
3. **Softness rule.** The frozen rule needed all six edges (3 lines x 2 mass rules). One of the six (line 0.105, enclosed-mass rule)
   already fails at 1 kpc, so only five edges exist; the spread x1.78 / x1.82 is therefore a lower bound on the true spread.
4. **Order of looking.** Before writing D-C I had seen the first six canonical t_medium values of the CFG744 JSON (they gave a
   largest L*_open of ~13.7 kpc); I had also seen that CFG760 records rms 0.16-0.17 at 7.6-9.5 kpc. D-C's closure prediction is
   therefore NOT independent of seen data. The SPARC edge itself (R7) was not seen before the run.
5. D-B numbers (c^2/a0 = 9.60e26 m canonical, 7.94e26 m alt) were computed by hand before the run and match the script.
