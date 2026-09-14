# G035 — THE ATTRACTOR TEST — VERDICT: KILL

**Rung 4 is now quantified: the Zimmerman temperature σ² = G·M_b/(2·r_M) is neither an
attractor nor even an equilibrium of the certified physics (Newtonian baryons + Newtonian
dust self-gravity). PAPER29's POSTULATED label is confirmed and sharpened.**

Instrument: certified. 11/11 static validations (V1 unit identity G·M_b = 2σ_t²r_M exact
on both footings; V2 real-SPARC closed loop; V3 field structure; V4 potential↔field
7.6e-4; V5 tracer orbit 2e-6; V6a/V6b FORCE DIRECTION (attractive, the failure class
this lane actually hit and caught); V7 inverse-square orbit bound; V8 numba≡numpy 1.7e-15).
Full suite: 58 runs, worst |dE/E| = 2.7e-5, dt-convergence twin agreement 0.2% (σ²) /
0.9% (r50), 98% of cells relaxed at t_end. NGC3198 real baryons (M_b = 6.2501e10 M_sun,
the G033 bundle pipeline value), r_M = 9.65 kpc, σ_target = 118.05 km/s (canonical);
alt-footing subset reproduces every pattern (σ² ratios within 0.03, same slopes).

## 1. The pre-registered verdicts (frozen before the suite ran)

- P1 (temperature): **FAIL** — σ_inf²/σ_target² spans 0.28–1.06 across the μ=0.3 grid;
  no cold or warm start lands in [0.8, 1.25]. Cold starts (σ_start ≤ 1.0) all cool to
  0.33–0.52; hot starts (1.5) overshoot only by leaving (r50 ≈ 22 r_M, f_esc 56%).
- P2 (radius): **FAIL** — r50/r_M spans 0.19–80.9 across the grid.
- P3 (equilibrium control): **FAIL — the strongest form of the kill.** The C2 control
  (isothermal r⁻² shape at exactly σ_target) is NOT an equilibrium: at t = 100 t_cross
  it has evaporated (f_esc = 0.37–0.51), expanded to r50 = 4.9–10.4 r_M, and cooled to
  σ²/σ_target² ≈ 0.32–0.33 — while its inner dispersion profile still reads ~σ_target
  (0.91–1.02 in 0.3–0.6 r_M). Material at the Zimmerman temperature in the combined
  well is UNBOUND: the well does not hold σ_target-temperature dust at r_M.
- Registered kill patterns: kill_T **FIRED** (σ_inf²(σ_start=1.5)/σ_inf²(σ_start=0.3)
  = 1.33 / 1.96 / 2.45 at R0 = 0.5 / 1 / 2 — memory of initial conditions, monotone,
  3/3 R0 columns); kill_R **FIRED** (r50 spans 4.8–47× across R0 at fixed σ_start).

## 2. THE TRANSFER FUNCTION (canonical; the registered deliverable)

σ_inf²/σ_target² (rows σ_start, cols R0/r_M):
```
 μ=0.1        R0=0.5   R0=1.0   R0=2.0        r50/r_M
  σ_start=0.3   0.310    0.388    0.371          0.242  0.523  1.182
  σ_start=0.5   0.329    0.405    0.350          0.319  0.640  1.384
  σ_start=0.7   0.361    0.389    0.275          0.408  0.752  1.906
  σ_start=1.0   0.369    0.370    0.327          0.583  1.197  7.591
  σ_start=1.5   0.750    0.943    1.064          2.325 28.540 86.100
 μ=0.3 (PRIMARY)
  σ_start=0.3   0.515    0.455    0.424          0.193  0.474  1.111
  σ_start=0.5   0.474    0.495    0.396          0.274  0.588  1.319
  σ_start=0.7   0.467    0.460    0.329          0.360  0.739  1.761
  σ_start=1.0   0.446    0.391    0.325          0.504  1.095  5.177
  σ_start=1.5   0.683    0.894    1.039          1.715 22.318 80.874
 μ=1.0
  σ_start=0.3   1.060    0.807    0.590          0.155  0.350  0.921
  σ_start=0.5   1.147    0.814    0.577          0.192  0.455  1.129
  σ_start=0.7   1.099    0.822    0.485          0.246  0.578  1.496
  σ_start=1.0   0.965    0.643    0.360          0.357  0.818  2.592
  σ_start=1.5   0.769    0.712    0.804          0.617  3.406 53.218
```

## 3. How far the theory is from an attractor (exact)

1. **The relaxed temperature is ~0.35·σ_target², not σ_target².** Cold/warm starts
   (σ_start ≤ 1.0) relax to σ²/σ_target² = 0.33–0.52 (μ=0.3) and 0.28–0.41 (μ=0.1)
   — the same factor-~3 deficit the audit found in K001, now with a certified
   instrument in physical units with real baryons.
2. **The confinement radius is the initial radius** (the audit's 0.53·R0, refined):
   for σ_start ≤ 0.7, r50/R0 = 0.39–0.95 with no trace of r_M; the equilibrium size
   is set by (σ_start, R0), not by a0. Hotter starts forget R0 only by dissolving
   (r50 ≫ r_M, f_esc → 1): there is no confined attractor to forget them TO.
3. **NEUTRAL coverage map (partial convergence, registered):** the only cells inside
   the temperature window [0.8, 1.25] are μ=1.0 at R0=0.5 (0.77–1.15) — but those
   same cells sit at r50 = 0.15–0.36 r_M, outside the radius window. The only cells
   inside the radius window are the cold/warm σ_start ≤ 1.0, R0 ∈ {1, 2} columns at
   μ ≤ 0.3 — at σ² ≈ 0.33–0.50, outside the temperature window. **The overlap of the
   two pre-registered windows over all 45 cells is EMPTY: no initial condition
   converges to (σ_target, r_M) in both temperature and radius.**
4. **S1 (the μ-dependence):** the relaxed temperature tracks neither the Zimmerman
   value σ_target² (baryon-only well) nor the combined-well virial null
   (1+μ)·σ_target²: the dust sits at ≈ 0.35–0.39 × (1+μ)σ_target² at every μ
   (0.388/0.450/0.772 for μ = 0.1/0.3/1.0 at R0 = 1 — ratios to the null 0.35/0.35/0.39).
   The Zimmerman formula is not the μ→0 limit of the relaxation either (μ=0.1 → 0.39,
   not 1.0). Violent relaxation in this well does NOT produce the virial temperature
   of any well — the relaxation is incomplete (t_end = 50–200 t_cross ≪ 2-body
   relaxation time); the settled state is a cooling, expanding transient, not an
   equilibrium.
5. **S2 (the rung-5 mass budget):** max M_d(<r_M)/M_b = 0.30 over the whole μ=0.3
   grid (identification requires 1.0). Consistent with 3–4: the dust never
   accumulates at r_M.
6. **Alt footing (a0 = 1.1279e-10):** same matrices (σ² ratios within 0.03 of the
   canonical columns, e.g. primary diagonal 0.470/0.442/0.325 and r50 pattern
   0.53–0.75–1.7/5.2): the kill is footing-independent, as it must be — the deficit
   is a dynamical statement about Newtonian wells, not about where r_M sits.

## 4. What this does to the theory

- Rung 4 ("the cold sector equilibrates at σ² = GM_b/(2r_M)"): **the dynamical
  foundation is dead.** Under the certified physics (dust feels only baryons + its
  own gravity — the registered test), σ_target² is not an equilibrium (P3 fail:
  the control evaporates) and no IC converges to it (P1/P2 fail, empty overlap).
  The temperature must be POSTULATED (PAPER29's label stands) or derived from
  something outside this physics (e.g. the L247 constitutive-law route).
- Rung 5 (the identification): the algebraic identity σ² = sqrt(GM_b·a0)/2 and its
  consequences (isothermal ρ ∝ r⁻², BTFR, deep RAR) are untouched — they are exact
  algebra GIVEN the temperature (G031). But the mass budget (S2: ≤ 0.30 vs 1.0)
  confirms there is no dynamical population of the phantom density in these runs:
  the identification is a definition of the temperature, not an equilibrium state
  of the certified N-body system.
- Rungs 0–3 and the pincer (§3 of the theory doc) are untouched: this kill is about
  the DYNAMICAL ORIGIN of one constant, not about the algebra or the measurements.
- The audit (PAPER29, commit a1febe8b8) is **confirmed and strengthened**: K001's
  r50 = 0.53·R0 pattern is reproduced (0.39–0.95·R0 for cold starts at every μ),
  and its "settled dispersion is half the target" is refined to ~0.35–0.45 of
  target with the C2 control showing the target is not even an equilibrium.

## 5. Honest instrument history (both runs recorded)

Run 1 (58 cells, commit 1 instrument): verdict INSTRUMENT-FAIL — the registered PE
clamp at XMAX = 60 r_M mis-bookkept the exact log-tail potential of escapers
(dE/E up to −0.42 in the C2 control; the flat-v_b tail potential grows as ln r, so
clamping it drops real PE). Fix: exact closed-form log tail at ALL radii (no clamp;
reference φ(60 r_M) = 0 kept), plus an encounter-time term in the step criterion for
hot cells. Verified on the three worst offenders: dE improved to ≤ 2.6e-6 with
physical outcomes unchanged (σ² within 0.002, r50 within 2%). Run 2 (this file):
same 58 cells, instrument gates PASS (energy_ok True, dt-convergence True, 98%
relaxed), verdict KILL on the frozen thresholds. The run-1 verdict (after removing
the instrument gate by hand) was also KILL on the same patterns — the instrument
fix changed no conclusion, only the certificate.

## 6. Reproducibility

*(N-count note: the pre-registration's "59 runs" double-counted the dt-convergence
twin; the executed suite is 58 runs.)*

- Engine: `G035_attractor_test.py` (numba O(N²) KDK leapfrog, adaptive dt = η·min(tau,
  eps/v), η=0.05; numpy fallback identical to 1.7e-15). Seeds registered per cell.
- Raw matrices: `G035_transfer_function.json` (all 58 runs with light curves).
- Suite logs: `G035_suite.out` (run 1), `G035_suite2.out` (run 2, the verdict run).
- Constants: NGC3198 M_b = 6.2501e10 M_sun (G033 bundle, max enclosed baryons),
  N = 2000, eps = 0.08 r_M, μ ∈ {0.1, 0.3, 1.0}, σ_start ∈ {0.3, 0.5, 0.7, 1.0, 1.5},
  R0 ∈ {0.5, 1, 2} r_M, t_end = 50–200 t_cross(r_M) (50·R0 crossing times), both a0
  footings (9.3619e-11 / 1.1279e-10 m/s²).
