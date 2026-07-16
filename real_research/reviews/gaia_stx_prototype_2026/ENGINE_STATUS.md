# Gaia-Asteroid s̄^TX Engine — Status & Architecture (2026-07-06)

**Goal:** an independent, public-data fit of the framework's *fixed-direction* gravity-sector
Lorentz-violation coefficient s̄^TX from Gaia asteroid astrometry — the one channel where we have
agency (planetary normal points are custody-walled; Gaia asteroids are public).

## FOUNDATION — BUILT & VALIDATED (this session)

| Piece | Status |
|---|---|
| Gaia archive access (astroquery/TAP) | ✅ reachable; real data queried |
| Real dataset characterized | ✅ **158,152 asteroids, 23.3M observations, 2.8-yr baseline (DR3)**, ~148 obs/asteroid, ~0.5 mas |
| Force model (REBOUND 5.0 + ASSIST 1.2.3) | ✅ installed; **full JPL DE440 + planets + asteroid perturbers + GR-EIH + non-grav** |
| JPL ephemeris files | ✅ downloaded (DE440 112 MB + sb441-n16 645 MB) |
| ASSIST baseline integration | ✅ validated (time = **days since J2000**; custom force via `sim.additional_forces`) |
| SME physics | ✅ **Bailey–Kostelecký 2006 (gr-qc/0603030): Eq. 104** two-body LV acceleration; **Eq. 107 / Table 2** secular precession (s̄⁰¹ = cos Ω·s̄^TX + sin Ω·s̄^TY — the fixed-direction hook) |

## THE TWO FEASIBILITY UNKNOWNS — MEASURED (Fisher prototype g2)

- **Degeneracy efficiency ≈ 7% (×14 penalty)** — the per-asteroid orbit fit eats most of the signal but the fixed-direction cos Ω/sin Ω pattern survives. Not catastrophic.
- **√N scaling holds** (σ ∝ 1/√N cleanly) — the full 158k asteroids keep helping.
- **Yarkovsky ≈ ×2** — partially degenerate, *not* a hard floor.
- ⇒ realistic reach **~few×10⁻⁹** (framework a₀=9.36e-11 footing) — borderline, ~1 order from Hees's planetary ~10⁻⁹. An **independent public-data check**, likely not the gold constraint.

## FRAMEWORK-SPECIFIC (used at every applicable place)

- a₀ = **9.36×10⁻¹¹** (canonical, ρ_DE) **and 1.13×10⁻¹⁰** (alt) — both carried.
- Preferred frame = **CMB rest frame**; boost V_cmb = 369.82 km/s, β_cmb = 1.233×10⁻³, toward the **CMB apex** (RA,Dec = 167.94°, −6.94°).
- Fixed-direction lock: s̄^TY/s̄^TX = −0.214, s̄^TZ/s̄^TX = +0.125 → **one-parameter fit**.
- Framework **prediction** (per-body, 1/|a| ladder): s̄^TX(body) = (a₀/2|a|)·β_cmb·n_X; asteroids at r~2.5 AU → smaller per-body value; the **universal amplitude** the ensemble returns is the decidable quantity.
- Universal-vs-per-body fork carried explicitly.

## ARCHITECTURE (the clean build)

1. **Data** — astroquery pull of `gaiadr3.sso_observation` (RA, Dec, epoch, σ, Gaia position) for a well-observed asteroid sample.
2. **Baseline orbit** — ASSIST integrates each asteroid (Sun+planets+perturbers+GR+non-grav). Fit 6 elements (+ Yarkovsky) to the Gaia positions.
3. **SME term** — add the framework s̄^TX perturbation. Two equivalent routes: (a) `sim.additional_forces` implementing Eq. 104 (boost s̄^TK terms, V=V_cmb), or (b) the analytic B-K secular precession added on top (matches how Hees does it; sidesteps the C-force). **Route (b) preferred** for robustness.
4. **Global fit** — joint least-squares: per-asteroid elements (nuisances) + one universal s̄^TX amplitude (fixed direction). Schur-complement marginalization (validated in g2).
5. **Framework comparison** — fitted universal s̄^TX vs framework prediction, both a₀ footings.

## REMAINING (next phase) & HONEST CAVEATS

- Wire the SME term (route b) + build the real-data joint fitter; run on a real Gaia asteroid sample → first real number.
- **Cross-check Eq. 104's exact O(1) coefficients against Hees+2015** before any publication claim (flagged).
- Planetary perturbations add a real per-asteroid precession = extra nuisance → true degeneracy somewhat worse than the g2 ×14.
- Realistic outcome: a novel, reproducible, ~few×10⁻⁹ independent constraint — publishable as *"an independent Gaia-asteroid limit on fixed-direction gravity-sector Lorentz violation"*, testing the framework's s̄^TX prediction. Likely **not** beating the planetary bound.

## Scripts (uncommitted, this dir)
`g1_gaia_characterize.py` (real data) · `g2_fisher_prototype.py` (systematics measured) ·
`g3_sme_force.py` (framework SME force + validation) · `ephem/` (JPL DE440 + sb441).

## REAL-DATA MILESTONE (2026-07-06, later)
- Pulled **1,309 real Gaia DR3 observations** of asteroids 1,2,3,4,10,15,324 -> `real_sample.ecsv`.
- Epoch reference confirmed: `epoch_utc` = **days since JD 2455197.5 (2010.0)**; ASSIST wants days since J2000 -> convert t_assist = (2455197.5 + epoch_utc) - 2451545.0.
- **Precision reality check: median sigma_RA(systematic) ~ 1.7-2.1 mas** (not the 0.5 mas assumed).
  The systematic floor is CORRELATED and does not beat down like random noise -> **worsens the
  forecast**: realistic reach likely ~1e-8 (framework footing), ~10x from Hees's planetary ~1e-9.
  Honest verdict tightens: a **novel independent public-data check, NOT a competitive constraint**.
- Numbered asteroids are IN sb441 (ASSIST perturber ephem) -> initial orbits available; no IOD-from-scratch.

## IMMEDIATE NEXT (the fitter)
1. Hees+2015 coefficient cross-check (PDF didn't parse via fetch; get the exact <dω/dt>(s^TX) constant).
2. Orbit-determination fitter: ASSIST-integrate each asteroid from its JPL state, project geocentric
   RA/Dec at each Gaia epoch, residual vs observed, fit (initial state + global s^TX, fixed direction).
3. Inject-and-recover validation on real orbits, then the real s^TX fit + framework comparison.
