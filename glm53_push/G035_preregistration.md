# G035 — THE ATTRACTOR TEST (pre-registered)

**Rung under test: rung 4** — "the cold sector equilibrates at σ² = G·M_b/(2·r_M)".
Status per PAPER29 (commit a1febe8b8): **POSTULATED**. The audit's refutation of the
supporting N-body (K001) is recorded: K001 integrates Newtonian gravity in units where
r_M := 1 (a0 never enters its equations of motion), its own initial-condition runs give
relaxed r50 = 1.06 / 1.57 / 3.17 for start radii R0 = 2 / 3 / 6 — i.e. r50 = 0.53·R0:
the confinement radius is the INITIAL radius, not an attractor at r_M — and the settled
dispersion is half the target.

This pre-registration is **committed before any dynamics run of the suite is executed**.
The engine's static validations (V1–V4) and the constants block are the only code
executed between this file's commit and the suite launch.

---

## 1. The claim under test (exact)

σ_target² = G·M_b / (2·r_M),  r_M = sqrt(G·M_b / a0)  ⇒  σ_target² = sqrt(G·M_b·a0)/2.

**The KEY physics decision (registered):** the dust feels ONLY Newtonian baryon
attraction + its own Newtonian self-gravity. The phantom is the EQUILIBRIUM description,
not an extra force. The test is therefore: does Newtonian (real baryon field) +
self-gravity + violent relaxation PREDICT σ_target, or must it be postulated?

## 2. Instrument (frozen)

- **Galaxy:** NGC3198, baryon field taken from the REAL SPARC curve in the G033 bundle
  (`website/src/data/fluid_real_data.json`, 43 points, D = 13.8 Mpc).
  M_enc(r) = v_b(r)²·r/G from the curve's own baryonic speeds;
  **M_b = 6.2501e10 M_sun** (max enclosed baryons, the G033 pipeline value).
  Field used direction-averaged (spherical): g_b(r) = G·M_enc(r)/r², exact closed form,
  **no softening** (M_enc ∝ r³ at small r ⇒ g_b smooth at the origin).
  Extrapolation, registered: below the first curve point, solid-body (v_b ∝ r, M ∝ r³);
  beyond the last point (44.1 kpc), flat v_b (M ∝ r, g_b const). Dynamics live inside
  ~2.5 r_M = 24 kpc ≪ 44.1 kpc: the extrapolated region touches only escapers.
- **Units: PHYSICAL (SI internally), no r_M := 1 trick.** Lengths in m, times in s.
  Code scaling for speed only: length unit = r_M, time unit = t_cross(r_M) = r_M/σ_target,
  mass unit = M_b ⇒ G_code = 2 exactly (asserted at runtime); the a0-footing choice enters
  the dimensionless equations through the REAL baryon profile sampled at r/r_M
  (the two footings are genuinely different dynamical problems).
- **Dust:** N = 2000 equal particles, mass m_d = μ·M_b with **μ ∈ {0.1, 0.3, 1.0}**.
  μ = 0.3 is the PRIMARY suite (the registered instrument of K001, the rung's cited
  N-body); μ = 0.1 (tracer) and μ = 1.0 (dust-dominated) are registered secondary
  diagnostics with their own transfer functions.
- **Softening:** Plummer eps = 0.08·r_M on the dust-dust force only
  (canonical: 772 pc; alt: 703 pc) — smaller than r_M/10 as required.
- **Integrator:** KDK leapfrog, dt = t_end/12000, one force eval/step,
  t_end = 50·R0/σ_target (i.e. **50 crossing times at R0 = r_M by definition**,
  t_cross(r_M) = 79.9 Myr canonical / 69.5 Myr alt). ≥ 50 internal dynamical times
  for every R0 in the suite (checked: 57–114).
- **ICs (C1, the attractor suite):** uniform sphere radius R0, velocities isotropic
  Gaussian with per-component dispersion σ_start, zero net momentum, no rotation.
  **σ_start/σ_target ∈ {0.3, 0.5, 0.7, 1.0, 1.5}**, **R0/r_M ∈ {0.5, 1, 2}**.
  Seeds fixed per cell (10000 + 100·μidx + 10·σidx + R0idx) — deterministic reruns.
- **ICs (C2, equilibrium-existence control):** dust ρ ∝ r⁻² on [0.25, 2.5]·r_M
  (r uniform: M ∝ r), velocities Gaussian at exactly σ_target, same N, μ grid.
  Registered caveat: with μ·M_b < 2.5·M_b this is the isothermal SHAPE at the target
  temperature, not the full singular isothermal sphere (which would need M_d(<r) = 2σ_t²r/G);
  C2 measures whether the temperature and shape HOLD, not exact stationarity.
- **Canonical suite:** 3 μ × 5 σ_start × 3 R0 = 45 C1 runs + 3 C2 = 48.
  **Alt-footing confirmation subset (a0 = 1.1279e-10):** 9 C1 (μ=0.3 σ-grid @R0=1;
  μ=0.3 diagonal @R0=0.5,2; μ=0.1, μ=1.0 diagonals) + 1 C2 = 10.
  **One dt-convergence run:** μ=0.3, σ_start=0.5, R0=1 at dt/2 (24000 steps), canonical.
  Total 59 runs.

## 3. Measurements (frozen)

At t_end (and every 300 steps for the light curve), ALL particles (no truncation —
confinement is part of the claim):
- **σ_inf²** = variance of the 1D velocity components (COM-subtracted), averaged over x,y,z;
- **r50, r90** = median / 90th percentile of the 3D radii;
- **f_esc** = fraction at r > 10·r_M; density slope dlog ρ/dlog r over 0.3–3 r_M;
  1D dispersion profile σ(r);
- **Relaxed flag:** |Δr50|/r50 < 0.15 and |Δσ²|/σ² < 0.20 between 0.85·t_end and t_end;
- Energy drift dE/E as an instrument diagnostic (Φ_tail approximated past 30 r_M;
  diagnostic only, not verdict-gating).

Reference numbers (both footings, from the bundle's own M_b):

| footing | a0 (m/s²) | r_M | σ_target | t_cross(r_M) | eps |
|---|---|---|---|---|---|
| canonical | 9.3619e-11 | 9.647 kpc | 118.05 km/s | 79.9 Myr | 772 pc |
| alt | 1.1279e-10 | 8.789 kpc | 123.67 km/s | 69.5 Myr | 703 pc |

## 4. Pre-registered verdicts (frozen BEFORE any run)

Applies to the canonical-footing PRIMARY suite (μ = 0.3, all 15 (σ_start, R0) cells),
with the σ-ratio window applied to the TEMPERATURE (σ²) as the theory's claim is σ²:

- **P1 (temperature attractor):** 0.8 ≤ σ_inf²/σ_target² ≤ 1.25 in EVERY cell.
- **P2 (radius attractor):** 0.5 ≤ r50/r_M ≤ 2.0 in EVERY cell.
- **P3 (equilibrium exists — the control):** C2 (μ = 1.0) at t_end holds
  σ²/σ_target² ∈ [0.8, 1.25], r50/r_M ∈ [0.5, 2.0], and the 1D dispersion profile stays
  flat at σ_target within 25% over 0.3–2 r_M; AND the C1 diagonal (σ_start = σ_target)
  does not drift by more than 20% in σ² from 0.85·t_end to t_end.
- **P4 (transfer function, always recorded):** full matrices
  σ_inf²(σ_start, R0; μ)/σ_target² and r50(σ_start, R0; μ)/r_M.

**PASS (rung 4 → DERIVED-ATTRACTOR):** P1 ∧ P2 ∧ P3.
If P1∧P2 hold at μ = 0.3 and 0.1 but not 1.0, verdict is
**PASS (tracer-scope)** with the μ-dependence quantified against the registered
combined-well null σ_cw² = (1+μ)·σ_target².
**KILL:** P3 fails (σ_target is not even an equilibrium of the combined well) — OR —
P1/P2 fail with the systematic IC-memory pattern: at fixed (μ, R0),
σ_inf²(σ_start=1.5) > 1.25·σ_inf²(σ_start=0.3) monotone in σ_start for ≥ 2 of 3 R0,
or r50(σ_start=0.3) spanning > 1.5× across R0 at fixed σ_start (r50 tracks R0 —
the audit's 0.53·R0 reproduced). The kill is quantified by the recorded transfer
function and by how far the theory is from an attractor.
**NEUTRAL:** partial convergence — the exact converging (σ_start, R0) map is reported.

Secondary registered analyses:
- S1: σ_inf²(μ) vs the Zimmerman value σ_target² (baryon-only well) vs the combined-well
  virial null σ_cw² = (1+μ)·σ_target² — does the relaxed temperature track the well
  actually present, and is the Zimmerman formula the μ→0 limit only?
- S2: mass-budget consistency — rung 5's identification requires M_d(<r_M) = M_b at
  equilibrium; compare with measured M_d(<r_M) at t_end in cells that converge.

Honest-instrument failure modes (would invalidate, and would be reported as such):
energy drift |dE/E| > 5e-2 in a run, dt-convergence run disagreeing with its twin by
> 5% in σ_inf² or r50, or a relaxed-flag failure rate > 1/3 of cells at t_end.

## 5. What is NOT claimed

No claim is made about MOND forces (none are present — registered physics is Newtonian
baryons + Newtonian dust), about the EFE cap (external fields absent by construction),
or about cluster scales. A KILL here does not touch rungs 0–3 (measurements/algebra);
it removes the dynamical foundation of rungs 4–5's temperature and relegates the
identification to the constitutive-law route (L247) or to postulate.
