# CFG640 FROZEN CRITERIA: framework-native 1024³ shear test of the condensed-baryon source as a PHASE law (H-CB-phase)

Committed alone, before any CFG640 validation run and before any CFG640 production run. Date: 2026-10-12.
This file is never edited; dated disclosures go in the README.

## 0. Disclosure: what was seen before this file was written

- **CFG596's canonical RESULT** (41efda383): candidate B (phantom sourced by all retained baryons) EXCLUDED on raw KiDS-1000
  (Δχ² +68.7, robustness minimum +43.9, T-OWN pass, NZ1 bites); DES Y3 +22.4 NOT DIAGNOSTIC; own boost 1.19 / 1.25 / 1.21 at
  k 0.3 / 0.5 / 1. CFG596 P2 (alt) was stopped by owner request; no alt verdict.
- **CFG634's results** (1fea20013): H-CB NOT DECIDED (reservoir-limited); its halo-model reading (context only) flips the excess
  to a deficit, not robustly.
- **CFG636's criteria (89aeaae12) and its 256³ PREVIEW** (924a9d5c8; census cap 0.10 inside catchments, field weight 1.0):
  P_grav/P_S0 at z = 0, k 0.3 / 0.5 / 1 = 1.058 / 1.100 / 1.091, G = 0.112 at 256³. CFG636 C1 (1024³) is RUNNING; its result
  was NOT known when this file was written.
- **astra's phase-source review** (bd8981d3d, `sol61_push/phase_source_closure_2026_10_12/RESULT.txt`): the CFG596/636
  representation maps a hot and a condensed state with equal baryon density to the same source; a phase-sensitive test needs
  a separately carried condensed component, and requirements (i)–(iii) of its Route 1.
- **The split-rule design table** (`cfg640_split.py` → `.out/.json`, no simulation) was computed before freezing: with the frozen
  geometry f_c − 0.10 ≤ 6e-4 everywhere (cooling of hot gas spread to the catchment radius is negligible), so f_c ≈ the census floor;
  the r_M-truncation bracket would raise f_c to 0.325 in lM 13 catchments (a large lever, NOT used, disclosed in §1).
- **Settings:** κ = ½ is FITTED. Footings (9.3603e-11 / 1.1312e-10) never pooled. "Cold energy" throughout; its MASS is still
  required; no particle species. Not "theory closed". Nothing here may say the data favour the framework. No ΛCDM or
  standard-MOND yardstick in any verdict.

## 1. Hypothesis, split rule and engine

- **H-CB-phase:** the law's phantom is sourced only by CONDENSED baryons (stars + cold gas), carried as a separate state; HOT
  baryons source ordinary gravity only. Ordinary gravity reads all mass, unchanged.
- **Representation:** each PM particle carries f_d ∈ [0, 1], the condensed fraction of its baryon share (float16); hot = 1 − f_d.
  f_d = 0 at z_i = 49 (diffuse).
- **Phase law (no new tuned constant):** at every dynamical census refresh (the existing every-10th-call catchment refresh of
  cfg596_pm.py; snapshot / diagnostic calls never change f_d), each particle whose nearest grid point lies in catchment k gets
  f_d ← max(f_d, f_c,k). f_d is never lowered (condensation irreversible; no reheating/feedback model). Particles outside every
  catchment keep f_d.
  - f_c,k = f_floor + (f_ret,k − f_floor) χ_k, f_floor = 0.10 (census floor, stars + cold gas; CFG515 / CFG634 HC-1), f_ret = the
    census fret_of (unchanged).
  - χ_k = min(1, r_cool/R_k): hot gas of mass (f_ret − 0.10) f_b M_ta, isothermal at T = μ m_p V²/(2k), V⁴ = G M_ret a0 (the law,
    FLAT branch, per footing), ρ_hot ∝ r⁻² out to the PHYSICAL catchment radius a R_k/h; t_cool(r) = 3(n/n_H) k T/(2 (n_e/n_H) n_H Λ)
    equated to t_dyn = r/V (the record's SIS free-fall time, CFG369 / CFG638).
- **Inherited ingredients (context, not tuned here):** Λ(T) = Tozzi & Norman (2001) Z = 0.3 Z_sun fit as carried by the record
  (cm12 → CFG369/370) with CFG370's corrected 1e-22 normalisation; μ = 0.6, n_e/n_H = 1.17, n/n_H = 2.3 (cm12 / CFG370);
  collisional-ionisation cooling only (no UV background: irrelevant above 1e5 K, and every catchment with hot gas has kT ≳ 0.09 keV ≈ 1e6 K);
  the census f_ret and floor (CFG515); the Δ_ta(z) table (ΛCDM shell ODE, as in CFG596).
- **Knob-like structural choices (declared, frozen, not tuned):** (K1) the hot-gas truncation radius = the catchment radius R_k
  (where the PM measures M_ta and applies the source) — the r_M alternative is a large lever in groups and is NOT run;
  (K2) t_dyn = r/V rather than the age; (K3) Z = 0.3 Z_sun; (K4) irreversibility; (K5) unresolved sub-RMIN haloes carry no
  condensed baryons unless their particles later enter a catchment (a resolution bias, low). None is varied in the verdict.
- **Source:** the MOND input is f_b ρ_d/ρ̄ with ρ_d the CIC deposit of the particles' f_d (normalised by the mean TOTAL particle
  density); everything downstream (ν_mono, s_ph, switch RES, R5 shell draw, supply, cap) is cfg596_pm.py verbatim. The census edge
  (x_supply) uses f_c,k in place of f_ret,k (as CFG636 did with its cap).
- **Engine:** `cfg640_pm.py` = `CFG596_lean_pm_1024/cfg596_pm.py` at 6323b630f + the above. `CFG640_SOURCE=b` restores cfg596's
  all-retained-baryon source on the original code path.
- **Not implemented (stated):** astra's Route 2 conversion-energy term −∫μ_d Γ dx (no W_int is specified), and any thermal
  evolution of the hot phase beyond the instantaneous cooling criterion. A pass would not establish a complete phase dynamics.

## 2. Validation gates (before production; 256³ L100 NSEED 512 RMIN 0.78125, lean, ONE process ≤ 3 GB, nice 10)

- **V-R:** VBr = cfg640_pm.py with `CFG640_SOURCE=b` must equal CFG596 VLr (`cfg596_work/VLr`) BIT FOR BIT (every stored snapshot
  quantity, all six snapshots, difference exactly 0). Fail → no production.
- **V-P (phase pair, on VPh's z = 0 particles and f_d):** (b) two states with identical positions, momenta and total density —
  A: f_d as evolved; B: f_d = 0 for particles with x < L/2 (same baryons, hot instead of condensed) — must give DIFFERENT
  phantom sources (src differs), while the old representation (`b` path) gives IDENTICAL results for A and B (bit for bit);
  (i) moving only the f_d = 0 particles (fixed ρ_d, changed ρ_h) leaves the condensed MOND input bit-for-bit unchanged while the
  total density changes; (iii) f_d ≡ 0 gives a source of exactly zero. Any failure → no production.
- **V-H (smoke):** VPh = `phase`, same configuration, must complete; P_grav/P_S0 at k 0.3 / 0.5 / 1 (S0 = CFG596 VLs) reported
  as a PREVIEW, NOT a verdict.

## 3. Production runs (NOT started by this lane's author; owner or orchestrator launches)

- H1 = phase RES canonical, then H2 = phase RES alt: L = 100 Mpc/h, N = 1024, NSEED 1024, seed 359, RMIN 0.78125, lean, spill,
  14 threads, nice 10, the 150-step grid and snapshots of CFG596. S0 = CFG596 P0 (shared, read only).
- **Start condition:** CFG636 C1 has finished AND been scored (cfg636_native_results.json written with its canonical run); no
  cfg596_pm.py / cfg636_pm.py / cfg640_pm.py process running; free + inactive memory ≥ 48 GB. Nothing is killed.
- Abort rule unchanged (RSS > 50 GB or swap growth > 4 GB). Optional MUTATE run HM (`b`, canonical) must reproduce CFG596 P1.

## 4. Statistic, data and verdict: identical to CFG636 (89aeaae12), i.e. CFG596 (f6c27d401) + growth gate

- **Scorer:** `cfg640_native.py` = `cfg636_native.py` pointed at H1/H2 (framework) and CFG596 P0 (S0); nothing else changed.
- **Data:** raw KiDS-1000 and DES Y3 ξ± with published covariances, n(z), cuts. **Support cut:** ≥ 90% of the integrand in
  [k_lo, k_hi], k_hi = πN/(4L); N_kept < 10 → NOT DIAGNOSTIC.
- **Models:** framework = the run's measured gravitating P(k, z) at z = 0, 0.5, 1 (CFG592 'F' path); S0 = P0's particle P.
- **Statistic:** Δχ² = χ²_min(framework) − χ²_min(S0) per survey and footing, IA marginalised; positive = framework worse.
- **Robustness set:** widen2, noIA, DESI distances, held. **Classes:** EXCLUDED (Δχ² ≥ 9 and robustness minimum ≥ 9);
  TENSION (Δχ² ≥ 4); CONSISTENT (Δχ² < 4 and robustness maximum < 9); NOT DIAGNOSTIC otherwise / N_kept < 10 / failed T-OWN.
- **T-OWN tooth and NZ1 MUTATE:** unchanged (`CFG596_MUTATE=1` pass run FIRST).
- **Growth gate:** at z = 0, G = max_{k ≤ 1} |P_grav/P_S0 − 1| ≤ 0.10; a deficit fails like an excess.
- **Verdict per footing:** FAIL if any diagnostic survey is EXCLUDED or G > 0.10; PASS (shear side) only if CONSISTENT on ≥ 1
  diagnostic survey, none EXCLUDED or TENSION, and G ≤ 0.10; a shear-side pass needs BOTH footings. Otherwise as classed.
- **Reported only:** f_d statistics per snapshot (mean, nonzero fraction, condensed input mean); the comparison with CFG636's
  cap result; the z = 0.5 / 1 growth numbers.

## 5. Inherited ΛCDM-calibrated ingredients (flagged, as CFG596)

EH no-wiggle IC spectrum at σ8 = 0.811; flat w = −1 background; Δ_ta(z) table; survey nuisance priors; massless neutrinos.
No HMcode, no BAHAMAS, no halo-model mass function in any verdict.
