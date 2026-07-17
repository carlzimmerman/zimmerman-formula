# SYNTHESIS — The MI Orbit Integrator (2026-07-16)

**What this is.** The first numerical instrument that integrates a point mass through a
real modified-inertia theory: the published covariant MI action's nonlocal kernel
K(□_u/a₀²) (Herglotz–Nevanlinna positive measure, ‖K‖≤1, causal-retarded, v11 sum rule
∫dμ/|t|=1), evaluated as a memory integral over the body's own past trajectory. Nobody
else has a concrete MI kernel, so no such integration has existed before. **It is not a
proof of the framework** — it is an instrument that makes the theory's orbital
predictions forced and falsifiable. No output uses "proves" language.

**Files (all in this directory; frozen repo untouched, read-only honored):**
`mi_integrator.py` (engine, exit 0, 36/36 gates, 53 s) · `mi_integrator.out` (banked
gate log) · `EOM_DERIVATION.md` (every step tagged PUBLISHED / DERIVED-HERE /
CONSTRUCTED-HERE(gated), traced to operator_definition.py v4 Lane B, the v11 sum-rule
arc, rb1–rb3, mi_offcircular_completion_SPEC.py, wb_dr4_prereg_framework_curve.py) ·
`applications.py` + `applications.out` + `APPLICATIONS.md` + 4 figures (17→22 app gates,
re-runs the engine suite at import) · `VERIFY_independent.py/.out` + `VERIFY.md`
(independent verifier, 19/19, overall **UPHELD, 0 downgraded, 0 refuted**).

---

## 1. Instrument status — what a referee needs to trust it

- **36/36 engine gates PASS, exit 0**; applications re-execute the full suite at import
  and refuse to run otherwise (gate_rerun.log). All thresholds computed in-script from
  re-derived quantities; no hard-coded results.
- **THE CIRCULAR GATE (C1), the trust anchor:** orbits integrated through the full
  memory machinery at y = 0.01–100 land on the published ν(y)=√(1+1/y) with max residual
  4.4e-9 (CANON) / 2.1e-8 (worst Mode-II corner) — at the RK4 floor (2.5e-9). **Both
  footings** (canonical a₀=9.36e-11 and alt 1.13e-10: 4.4e-9 on the full grid).
  The independent verifier *strengthened* this: circular speed found by **bisection on
  the dynamics** (ν nowhere in launch/init/bracket), verifier-chosen central mass,
  y-grid, and an independently constructed measure realization — the emergent ν equals
  the published law to ≤8e-9. The launch-at-the-answer hole is closed.
- **Newtonian limit (N1):** 4.3e-9 at y=10³, 1.8e-9 at y=10⁴ (closed-form deep-UV tail
  makes the high-y regime exact).
- **Balance laws derived from the action and gated:** angular momentum 6.1e-11; energy
  functional 1.8e-10; two-body **dressed** momentum Σmᵢμᵢaᵢ = M g_ext conserved to
  4.96e-18; **bare** momentum is *not* conserved — the measured CoM wander equals the
  analytic third-law defect integral to 2.8e-5 (ballistic, exponent 1.01; it is the
  theory, not the integrator).
- **Convergence:** RK4 order fitted 4.38 (verifier re-fit 3.85 on a fresh orbit);
  adaptive-vs-fixed agreement 2.6e-10; node-count monotone 1.7e-3 (N=8) → 2.8e-9 (N=64);
  memory-truncation and ζ-band demonstrated; eccentric app stable to 8e-6 dex under 2×
  steps + 2× horizon.
- **EOM not guessed:** operator structure extracted from the published action; verifier
  re-derived the mixture step K(z)=∫dν(s) z/(z+s) with its own tools (sum rule to <1e-9,
  K to <1e-7 over 13 decades), proved u·(D²u)=−|a|² sympy-identically on a generic
  worldline, and confirmed the first-moment closure / unimodular literal channel as
  PUBLISHED (rb1 / KERNEL_THEORY Thm B). One declared in-family instrument choice
  (Mode-I node-by-node dressing) is named, not hidden.
- **Startup honesty:** memory is over the past trajectory only (retarded poles);
  adiabatic two-pass pre-history init (the published quasistatic theorem's own
  assumption) with cold starts quoted as the startup systematic — with ~200-Gyr horizon
  memory the transient does not decay; pre-history is physics and is stated as such.
- **Failure discipline:** an earlier partial draft failed 14 gates when actually run;
  each cause was diagnosed (region-B quadrature floor, a stale hard-coded constant the
  banked script itself contradicts, sampling bias, a launch-shape confound, two gates
  encoding wrong physics) and rebuilt. Three app gates and two engine gates that encoded
  wrong bookkeeping/assumptions were replaced by gates on what the dynamics actually
  does, with the physics reported as findings (ledger in APPLICATIONS.md). No gate was
  tuned to pass.

**Measure freedom handled as mandated:** six realizations spanning the published class,
all constraint-checked (positivity, exact sum rule incl. analytic tail, sup K̃≤1,
retarded poles). The RAR grades them: CANON exact; TILT±0.025 alive (0.022 dex, inside
the 0.03-dex tolerance); POLE (0.37 dex), FLAT-MID (1.65 dex), FLAT-SHORT (3.65 dex)
**RAR-dead and quarantined** — the instrument-level reproduction of the banked rb2[3]
uniqueness theorem. Surviving freedom = {CANON, TILT±} × Mode-II memory corners
{ultralocal, H_Λ, gap}; the orbital-frequency corner is additionally quarantined by a
new finding (below). Every prediction is a **band over this alive class, both footings**.

## 2. Measure-independent results (the headline physics)

Identical across the alive class, every memory corner, both footings:

1. **Orbit shape barely moves systems off the RAR.** Eccentric galactic orbits
   (Plummer, e = 0→0.86): total offset 0 → [−0.0057, −0.0059] dex, sign **negative**
   (below the circular RAR); dSph/isotropic-dispersion ensembles: effective ν =
   **0.990–0.997** of the circular ν (verifier-corrected band), width <0.01 dex.
   Consequence: Jeans modeling with the published ν is accurate to <0.01 dex for any
   anisotropy within the kernel's closure freedom — the framework's galactic wins are
   *not* an artifact of the circular-orbit idealization.
2. **The planetary a₀/2 landmine is forced for the entire closure family.** Every alive
   member integrated through the full memory machinery leaves δg = a₀/2 (frozen corners:
   × the predicted ⟨g⟩/g_rms factor, 0.9969 vs 0.9968 at Saturn; tilts scale within
   0.39–2.6×). Vs INPOP/EPM 1σ bounds: Venus excluded 585× canon / 706× alt (band floor
   226×), Saturn 6686× / 8071× (floor 3333×) — **≥2.4 orders, measure-independent**.
   Agrees with laneK Reading A to <0.5%; laneK's Reading-C escape gates on the orbital
   frequency, *outside* the first-moment closure family that carries all published
   galactic wins — within that family no memory corner rescues the planets. New
   instrument finding: the strict two-body per-star MI-EFE reading **doubles** the
   landmine (1.999 × a₀/2, matching the static per-star algebra); real multi-planet
   geometry lands between a₀/2 and a₀ — either way excluded. This is a real, quantified
   wall, reported straight; per the honest-ceiling rule it discriminates between the
   framework's own doors, not framework-vs-ΛCDM.
3. **Orbit stability disfavors orbital-band memory corners.** The Mode-II corner placed
   at the orbital frequency is secularly unstable (monotonic pumping, +7.5%/cycle to
   escape) while slow/horizon-memory members show zero drift at 1e-10 — a falsifiable
   structural statement within the SPEC family, corroborated by adaptive-vs-fixed
   agreement at 2.6e-10.

## 3. Cross-checks vs banked numbers — all reproduced, none assumed

- **rb3 closure-B epicyclic law:** predicted −0.000209 dex vs measured −0.000216 at
  ε=0.075 (4%, gate 25%); ultralocal exactly 0; footing-stable.
- **Wide-binary prereg (`wb_dr4_prereg_framework_curve.py`):** the instrument's force
  law IS the banked per-star prescription to 8.9e-16 (static probe); the banked numbers
  re-derived, not copied — y_ext,N = 1.4647 (the stale 1.4525 appears nowhere in the
  lane), iso asymptote 1.1015, MG 1.1389, Milgrom-a₀ degeneracy 1.134. Dynamical runs:
  ultralocal γ_v = 1.0923 at 30 kAU, inside the banked 1.05–1.10 band — **agreement**;
  the 1.09-vs-1.1015 spread pinned as orientation-averaging convention of one curve.
- **Full closure fork (new):** γ_v ∈ [1.076, 1.151] canonical / [1.111, 1.169] alt, with
  horizon-memory members landing exactly on √ν(y_ext,N) = 1.1389 = **the MG/AQUAL
  asymptote** (0.01%; alt 1.1687 vs 1.1692). So **DR4 wide binaries discriminate closure
  members of this kernel, not MI-vs-MG per se** — this sharpens (and slightly weakens)
  the banked prereg: the banked 1.09 corresponds specifically to the ultralocal closure;
  γ_v outside ~[1.05, 1.17] cuts against the kernel on both footings. The horizon
  endpoint carries a stated init-convention dependence (steady pre-history = the physics
  with 200-Gyr memory).
- **laneK planetary Reading A:** 585× / 6687× reproduced to <0.5%.

## 4. What the instrument enables that was impossible before

Until now every MI statement beyond circular orbits was a scaling argument. With a
gate-validated memory-integral engine the theory can, for the first time, be *run*:

- **Non-circular predictions become numbers with error bands**, not hand-waves:
  eccentric-orbit RAR offsets, dispersion-supported systems, per-star EFE dynamics.
- **The measure freedom is measured**: the RAR pins the Herglotz class to CANON±tilt
  (rb2[3] reproduced at instrument level), and orbit stability itself excises the
  orbital-frequency corner — constraints on the kernel from dynamics, unavailable
  analytically.
- **Solar-system confrontation is now forced**: the a₀/2 landmine is no longer a
  quasistatic estimate but a trajectory-level, closure-family-wide exclusion with the
  two-body doubling as a new sharpened target.
- **DR4 interpretation is pre-computed**: the γ_v closure fork tells us in advance what
  a given DR4 number would select (a closure member) and what would kill the kernel
  (outside [1.05, 1.17]).
- Any future observable (streams, precession, dSph internal dynamics) can be integrated
  rather than estimated.

## 5. Ranked next runs

1. **Multi-planet integration** of the two-body-doubling geometry (Sun tail + several
   planets, 3D): pin the landmine between a₀/2 and a₀ by integration instead of
   argument — it is the one "argued, not integrated" claim in the bank (caveat 6).
2. **3D + orientation-averaged WB runs** with the velocity observable and the measured
   window-sampling wander (~0.5–0.8%/window-doubling, contracting within [1.05, 1.11]):
   turn the launch-shape confound into a quoted systematic for the DR4 γ_v band.
3. **Tidal-stream / Sgr-like run**: the bare-momentum defect (ballistic CoM drift,
   ~1.75% of v_rel on the test pair) is a qualitatively new MI observable no other
   formalism predicts — quantify it for a real progenitor.
4. **laneK Reading-C confrontation**: implement the orbital-frequency-gated evaluation
   *outside* the first-moment closure and test whether any member survives both the RAR
   and the planets simultaneously.
5. **Precession/perihelion channel at Mercury–Mars** from the same runs as (1) — a
   second, independent solar-system exclusion axis.
6. **Directional-EFE null** (banked kill switch): pure MI predicts exactly zero aligned
   RC asymmetry; the engine can now compute the closure-family band around zero.

## 6. Verifier corrections applied (none verdict-flipping)

1. APPLICATIONS.md dSph ratio band corrected 0.992–0.997 → **0.990–0.997** (its own
   TILT− entry is 0.9897; dex band and gates were already right). Carried here.
2. The verifier's own first WB-convergence check conflated timestep with averaging
   window; rewritten after decomposition (V-E2a/V-E2b) — verifier-side, not the lane's.
   All other en-route verifier failures (quad roundoff, float-cancellation sum-rule
   deficit, bisection bracket, two over-tight tolerances) were verifier bugs, fixed.

**Standing caveats (the lane's own, carried):** 2D planar, Newtonian-order
(v²/c² ≤ 2.5e-7), no lensing/disformal sector; adiabatic pre-history is an assumption
(the published theorem's own) and with horizon memory the cold-start transient never
decays — pre-history is physics; tilt planetary tails rest on a validated continuum
quadrature, not an orbit run; conventions (coplanar WB, virial-vs-time averaging at the
~0.001-dex level) are carried and printed, not eliminated. Everything off-circular is a
band over the papers' declared closure freedom — the instrument measures that freedom;
it does not resolve it.
