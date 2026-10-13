# CFG656 FROZEN CRITERIA: the X-COP cold-energy SUPPLY from the framework's own turnaround catchment and the measured gas, instead of CFG634's convention M_b(<R200)/0.90; CFG637's derived reservoir and T3/T2 gates re-scored

Committed ALONE, before any catchment, supply or gate number of this lane exists. Date 2026-10-12.

κ = ½ is FITTED. Footings canonical 9.3603e-11 / alt 1.1312e-10 m s⁻² (each reused gate keeps its own committed footing values) are
reported separately and NEVER pooled. "Cold energy" throughout; its MASS is still required; no particle species. Not "theory closed".
No ΛCDM halo shape or mass function and no standard-MOND yardstick enters any verdict. Nothing here says the data favour the framework.

## 0. Question and what was seen before freezing (disclosed)

Question: CFG637's T3 X-COP headline fail (η 1.820 / 1.679 candidate B; 1.494 / 1.661 H-CB; inner band H-CB 0.859 / 0.889 PASS)
rests on CFG634's per-scale supply convention for X-COP: catchment baryons = M_b(<R200)/0.90 with the retained core flat beyond
R200. Is the fail an artefact of that convention? This lane replaces it with the framework's own turnaround catchment, filled with
the MEASURED X-ray gas (extrapolated by a declared data-driven rule) plus stars, and re-runs CFG637's derivation and gates unchanged.

Seen before freezing: CFG637 README/criteria/scripts and its JSONs; CFG634's T3 code; CFG646 (census expelled fraction
ε = (1 − f_ret) f_b; placements DIFF primary, SHELL bracket); CFG515 census f_ret (fret_of caps at 0.90 for log M_ta ≥ 14.67
[Msun/h]); CFG654 native Δ_ta(z) table (z = 0: 11.831 vs cfg361 11.806, +0.21%) and native parameters (h 0.67403, Ω_cb 0.31285,
f_b 0.15431 → cold/b 5.481); CFG557 D1 (candidate B's switch = the turnaround ball). Data facts read: the T3 headline radius is
the outermost audit row, **1000 kpc for all 12 clusters** (≈ 0.45–0.57 R200, ≈ 0.7–0.95 R500), not R200; the X-COP gas profiles
(radius R/R500 × own R500, CFG450) reach r_max = 1.6–2.7 Mpc (≈ R200); the outer log-slope s = d ln M_gas/d ln r measured over
r ≥ R500 is 0.64–1.29 and over the last 3 points 0.32–1.20 (the profiles steepen outward). No catchment, supply, reservoir or η
of this lane was computed.

## 1. The catchment and the supply (declared)

**Turnaround radius (framework-native).** r_ta = [3 M_ta / (4π Δ_ta(z) ρ̄_m(z))]^(1/3), with Δ_ta(z) the CFG654 N0 native table
(`CFG654_independent_inputs/cfg654_delta_ta.json`, linear interpolation in z; candidate B's switch = the turnaround ball, CFG557 D1),
ρ̄_m(z) = Ω_cb h² ρ_crit,100 (1 + z)³ with CFG654's native Ω_cb 0.31285, h 0.67403. z per cluster from the X-COP R500 file
(Ettori+19). The cfg361 table is reported as a shift only.

**Catchment baryons.** M_ta = M_b,catch / f_b; M_b,catch = M_b,ret(<r_ta) / f_ret; M_b,ret(<r) = M_gas(<r) + M_star(<r) from the
measured profiles (below); f_ret = census (CFG515 `fret_census` applied to M_b,ret; expected 0.90, the cap, for every X-COP cluster;
reported). Solved as a fixed point in r_ta (relative change < 1e-10). **Supply = (1 − f_b)/f_b × M_b,catch** (5.364 × with f_b =
0.02237/0.14237). Reading of the census expulsion: CFG646's PRIMARY placement (DIFF) puts the expelled (1 − f_ret) of the catchment
baryons outside the one-halo region, so the measured X-ray gas inside r_ta is the RETAINED part and the catchment holds
M_b,ret/f_ret; the SHELL placement (bracket RET) leaves it inside r_ta, so the measured gas already includes it (f_ret → 1 here).

**Gas inside r ≤ r_max** (last finite measured point): log interpolation of the measured MGAS profile. **Beyond r_max:**
- **P (PRIMARY):** power law with the log-slope of the last 3 measured points, held to r_ta (CFG634's own `loglin_extrap`, now
  carried to the turnaround radius instead of R200).
- **HI (bracket):** power law with the least-squares log-slope over all measured points with r ≥ R500 (own file R500), held.
- **LO (bracket, data-driven steepening):** fit ln M = a + b L + c L² (L = ln r) to the points with r ≥ R500; slope
  s(L) = min(s_last3, b + 2cL), floored at 0 (flat beyond the radius where it reaches 0); integrated from r_max.
- **FLOOR (bracket, the data minimum):** no gas beyond r_max.

**Stars:** the stellar profile by CFG634's rule (log interpolation; beyond its last point the last-3 slope) to r_ta in P/HI/LO;
measured only (flat beyond its last point) in FLOOR. Clusters without a stellar profile: stars = gas × the median S/G ratio, taken at
each cluster's own radius over the clusters with stellar profiles (as CFG634's imputation, evaluated at r rather than R200).

**Supply brackets on the primary catchment:**
- **RET:** CFG646 SHELL placement: supply = 5.364 × M_b,ret(<r_ta) (catchment baryons = retained, f_ret = 1 in the catchment and
  in the derivation).
- **NAT:** CFG654 native composition: f_b = 0.15431 (cold/b 5.481), with cfg637_lib's background constants set to CFG654's native
  h 0.67403, Ω_m = Ω_cb 0.31285 for that run (catchment re-solved with that f_b).

## 2. Derivation and gates (= CFG637's, unchanged except the inputs above)

- **Derivation:** `cfg637_lib.derive` (Method A, self-similar secondary infall), PRIMARY settings unchanged: N 1600, ε 1, q 0.1,
  outer-first draw, phase-mixed read-out, a_obs = 1 (as CFG637; the catchment radius uses each cluster's z: disclosed difference).
  Inputs per cluster: M_ta (above), f_ret (census; 1 in RET), retained-core cumulative profile = gas + stars on 1 kpc … r_ta by the
  bracket's rule (gas ∝ r² inside the first data point, stars = gas × the S/G ratio interpolated in ln r over CFG634's audit radii
  and r_ta, as CFG637), flat beyond r_ta; source = gas + stars (candidate B) or stars (H-CB); kernel C4.nu_mono, a₀ = C4.A0[footing].
  The reservoir enters the gate as M_res,A(<r) × supply_gate / supply_A (CFG637 §1), supply_gate = this lane's supply.
- **Derivation brackets** on the primary supply (reported; they label, they do not decide): ε 0.5, q 0.05, q 0.2, uniform draw.
  Method B is not run (Method A is CFG637's deciding method).
- **T3 X-COP:** CFG634's `cl_model` / `t3_cell` / `t3_label` executed from CFG634's committed source with CFG637's single RD patch.
  Headline = outermost audit row (1000 kpc); inner band 200–420 kpc; b = 0.2 reported. η = M_HSE/M_model, median over 12, σ = SD/√12.
  **PASS** |η − 1| ≤ 0.20 on both footings; **FAIL** η ≥ 1.30 or ≤ 0.77 with ≥ 3σ on both; else TENSION. Per source (H-CB, B).
- **T2 groups (consistency):** the group catchment rule is NOT changed by this lane (the groups have no measured gas to r_ta; their
  rule M_bar/0.10 stays). PRIMARY T2 = CFG637's T2 re-scored from the same code and CFG637's derived group profiles; it must equal
  CFG637's RD|P|phase T2 (mean, Z) to 1e-9. **Bracket T2-CEN (reported):** the census f_ret applied to the groups as to X-COP:
  f_ret = fret_census(M_bar), catchment M_bar/f_ret, derivation with that f_ret, and CFG634's group supply edge read with M_bar/f_ret.
  CLOSES = |Z| < 2.
- **Diagnostic η(R200) (reported only, NO verdict weight):** M_FORW(R200) / [M_b(<R200) + the source's phantom at R200 (C4.nu_mono)
  + M_res(<R200)] for the old convention and the primary, R200 from the Ettori+19 file; M_FORW at R200 is the published
  reconstruction (beyond the audit rows).

## 3. Verdict rule (per source variant, Method A primary)

Let η₆₃₇ = CFG637's RD|P|phase headline η and η_P this lane's primary headline η, per footing.
- **CLOSES:** primary T3 headline PASS (both footings).
- **SHRINKS:** not PASS, and |η_P − 1| ≤ 0.75 |η₆₃₇ − 1| on both footings (the shortfall falls by at least a quarter).
- **ROBUST TO THE SUPPLY CONVENTION:** otherwise.
- Qualifiers: **BRACKET-DEPENDENT** if any of HI, LO, FLOOR, RET, NAT or the derivation brackets gives a different class;
  **INNER BAND BROKEN** if the primary inner band is FAIL where CFG637's was PASS; **CONSISTENCY FAIL** if primary T2 does not CLOSE.
  The T3 label (PASS / TENSION / FAIL) is reported with every class. A fail is a valid result and is verified as hard as a pass.

## 4. MUTATE and controls (all must hold, or the dependent result is VOID)

- **M-OLD (exact):** the OLD convention (CFG637's core: CFG634 log-extrapolation to R200, flat beyond; M_ta = M_b(<R200)/0.90/f_b;
  supply 0.1200/0.02237 × M_b(<R200)/0.90; f_ret 0.90; a₀ C4.A0), re-derived by this lane's script with cfg637_lib unchanged and
  scored by this lane's gate code, must reproduce CFG637's T3 RD|P|phase headline η, σ and inner-band η for both sources and both
  footings to 1e-9 absolute.
- **M-HALF (teeth):** the primary catchment baryons held fixed, the cold weight per baryon halved (f_b → 1/(1 + 2.682), supply × 0.5):
  η must not decrease in any source/footing cell (tolerance 1e-9), and must strictly increase (> 1e-6) in every source/footing cell
  whose primary run has a non-zero reservoir inside 1000 kpc in at least one cluster. (A cell with an empty primary reservoir has
  nothing to remove; reported as not applicable.)
- **C1:** supply_A = drawn + reservoir to 1e-9 relative; turned-around mass within 1.05% of M_ta, every run.
- **C-FP:** every catchment fixed point converged; the derivation's own r_ta is reported against the catchment r_ta.

## 5. Inherited ingredients (CONTEXT, not framework predictions)

Everything CFG637 §5 lists (seed slope, q bracket, spherical self-similar infall, X-COP hydrostatic reconstruction), plus: the
extrapolation of the measured gas beyond r_max (bracketed by HI / LO / FLOOR), the census f_ret function (CFG416/515), the
Ettori+19 redshifts and R200 (radius only, diagnostic), CFG654's native parameters.

## 6. Machine

One process, ≤ 1 GB, `nice -n 10`, OMP 1 thread; the waiting 1024³ queue and other lanes are not touched. No downloads.
Outputs: `cfg656_*.out`, `cfg656_*_results.json` in this directory (profiles npz regenerated by the derive script, not committed).
