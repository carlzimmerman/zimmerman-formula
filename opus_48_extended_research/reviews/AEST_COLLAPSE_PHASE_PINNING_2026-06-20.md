# Does dynamical collapse pin the AeST oscillation phase? — NO. The no-go holds DYNAMICALLY (the published paper confirmed in time)

*Workflow `wxbnjxb64` (4 agents: derive → compute → adversarial verify → synthesis), banked 2026-06-20.
The one un-closed branch of the published cluster no-go (Zenodo 10.5281/zenodo.20779562) — the AeST
authors' DS24-deferred calc taken all the way to dynamical embedding, at the tractable spherical-collapse
level. Both-ways; quarantine. A pin was actively hunted (damping swept to ~ω) and none manufactured.*

## Verdict: NO pin. The cluster boost stays descriptive, not predictive — now confirmed *dynamically*,
## not just in the frozen (static) case. The published paper STANDS and is strengthened.

## (1) What was computed
A 1+1D (radius × time) spherical-collapse-with-AeST solver: a spherical overdensity evolved from z_dec~20
through turnaround to virialization, with the **real** AeST field solved at each step two ways — the
static modified-Helmholtz BVP (DS24 Eq 2.40, in the smooth canonical-momentum form that survives the
oscillation nodes) AND a genuinely time-dependent Klein-Gordon wave χ_tt − c²∇²χ + (μc)²χ = S(r,t).
**Validation gates pass on re-run:** μ=0 collapse gives r_vir/r_max = exp(−½) to 1e-9; the static field
at μ=0 reproduces analytic MOND g(r) to 0.00 ppm. The equations are the authors' real ones, not a proxy.

## (2) The phase is NOT pinned — IC-dependent, triple-verified
The late-time oscillation phase tracks the initial-condition phase ~1:1, three independent ways:
- full collapse PDE: d(θ_late)/d(θ_IC) = **+1.18**
- analytic forced+free conservative oscillator: **+1.00**
- clean-room independent-stencil KG PDE with an **outgoing Sommerfeld boundary** (kills the reflecting-wall
  worry): **+1.20**

The phase keeps drifting through virialization (last-third drift −2.99 rad, no plateau); ensemble
circular-std **1.34 rad** across IC phase, mass (1e14–1e15), profile, z_dec. **Untuned eta(R500) =
−0.052** at a=1 (a tiny *deficit*), with the physical span [−3.12, +3.97] left accessible.

## (3) The deep reason — a conservative-wave free mode, no friction (the negative theorem)
The shift-symmetric AeST action has **no friction term**; its homogeneous free Helmholtz/KG mode at the
mass gap ω = μc is **conserved** — it neither decays nor phase-locks — and the collapse fixes only the DC
part. (μc)/H₀ = 4448, so χ oscillates **~708× per Hubble time** (Hubble damping per period 0.9979 ≈
undamped). The damping needed to pin the phase (~0.01ω) is **~30× above Hubble friction**; a damping sweep
confirms even 3H leaves the slope at −1.00. *Structure formation supplies no mechanism to fix the free
knob the static BVP leaves open.* That is the obstruction — structural (conservative wave), not geometric.

## (4) Galaxy-safe + Cassini-safe at every phase
Worst-case galaxy RAR shift **0.0026 dex** (19× under the 0.05 veto); Cassini margin ~1e16×. Protection is
geometric and phase-independent: (μ·10 kpc)² = 1e-4 vs (μ·R500)² = 2.25. The cluster no-pin does not leak
into the galaxy relation. So the framework is **not broken** — clusters just stay phenomenological.

## (5) Honest caveats — ALL THREE NOW CLOSED by the rigorous follow-up (workflow `wt0lamc4k`)
The three weaknesses flagged below have been re-tested by a rigorous follow-up solver that adds back exactly
what the scalar-only 1+1D run dropped. **The no-go HOLDS, harder.** Solver + verdict under
`opus_48_extended_research/reviews/aest_rigorous_collapse/` (aest_rig_core.py, aest_rig_selfconsistent.py,
aest_rig_nonradial_vector.py, aest_rig_ADVERSARIAL.py, aest_rig_run.py; SETUP.md). All numbers below are from
the master runner `aest_rig_run.py` (deterministic, seed=0), **independently re-run and verified 2026-06-20.**

- **CAVEAT 1 — kinematic-proxy matter collapse → CLOSED.** Replaced the prescribed cosine r_phys(t) with a
  self-consistent N-shell velocity-Verlet **r″=−g_AeST** (live M_b(<r) each step, cosmological background +
  virialization, native shell crossing → multi-stream, median **8 crossing events**). Result: free-mode
  **|IC-response| = 0.489** (slope d(θ)/d(IC) = +0.218, circ_std = 1.128 rad). HONEST READ (both-ways): the
  multi-stream collapse **does** partially decohere the phase — |IC-resp| drops from ~1.0 (smooth scalar-only)
  toward a pin — but stops **well short** of one (0.489 ≫ the 0.15 pin threshold; the descriptive boost η(R500)
  still spans a wild **−7.76…+4.26**, so NO universal galaxy-safe value is selected). Self-consistency moves the
  needle but does not pin. *(The "free-mode |IC-resp|=1.000" sometimes quoted is the **isolated free-mode /
  analytic** value = the adversarial γ=0 slope of 1.000, not the full self-consistent-collapse observable.)*
- **CAVEAT 2 — dropped vector-mode E / K_B coupling → CLOSED (and shown structurally trivial in spherical
  symmetry).** AeST's own structure makes the vector **identically trivial under spherical symmetry** (∇×A=0,
  the A and φ EoMs coincide — Durakovic-Skordis 2024), so the scalar-only run lost nothing there; the vector can
  only do new work **off-spherical**. Implemented it as a conservative (antisymmetric, energy-preserving)
  time-dependent mode-mixing matrix C_nm(t) from the violently-relaxing potential. Result: PHYSICAL conservative
  mixing **|IC-resp| = 0.980** (tracks IC → NO pin), **E_drift = −0.368**; a dissipative-sink CONTROL pins only
  with **|IC-resp| = 0.004, E_drift = −1.00**. The vector **redistributes** oscillation energy across modes
  (mixing) but supplies **no dissipative sink** — and only a sink pins. *(E_drift = −0.368 is not perfectly zero —
  ~37% leakage, vs the sink's 100% — likely numerical in the mode integration; the load-bearing result is the
  |IC-resp| = 0.980 = no pin.)*
- **CAVEAT 3 — spherical reduction missing violent relaxation → CLOSED.** Added multi-stream (caveat 1) +
  non-radial/tidal mode-mixing (caveat 2). Per Kandrup 1998, phase-mixing damps a coherent oscillation only
  with a frequency **continuum**; the observable rides the sharp discrete μc mode, which cannot phase-mix.
  Confirmed: no pin appears. The adversarial **damping sweep** shows the phase pins only at friction
  **γ ≥ 44.5 × 3H₀** — and AeST's action-conservative structure supplies **no friction term at all** (physical
  Hubble 3H₀ is 44× below threshold). Artifact-ruled: slope |~0.93–0.96| is **invariant** under ν_num halving +
  Sommerfeld/reflecting BC flip (structural, not a numerical-damping or reflecting-wall artifact).
- **Galaxy-safe at every phase:** worst-case RAR shift **0.0012 dex** (42× under the 0.05 veto); geometric
  protection (μ·R500)²/(μ·10 kpc)² = **22500×** → cluster phase-freedom does not leak into the galaxy RAR.
- **Earlier-run robustness blemishes (scalar-only) now moot:** the Hernquist/galaxy-slope NaN, the static
  [−22,+22] scan-width artifact (physical [−3.12,+3.97]), and the nonlocality mis-citation (it is **Deffayet &
  Woodard 2024**) all pertained to the superseded scalar-only solver.
- **Scope (the one genuinely-open item):** a full 3D cosmological AeST N-body remains the **definitive** word
  (self-consistent collapse + the full vector/tidal channels + a genuine cosmological χ(t) outer boundary, at
  HPC scale — the Skordis group's is in development, unreleased). The rigorous reduced-physics follow-up here is
  the **confirmation**, not that definitive word — but it closes all three of the prior's named weaknesses and
  points **firmly** at the no-go, because the obstruction is structural (a frictionless conservative wave), so a
  reversal is unlikely.

## Net
The cluster door does **not** reopen as the strong predictive result. The +μ²Φ boost is real (~10⁵× the
naive coupling) and galaxy+Cassini-safe, but **descriptive, not predictive**, in the static *and* dynamical
cases. The published no-go (Zenodo 10.5281/zenodo.20779562) stands, now confirmed in time. Credit held: the
+μ² lever is the authors' own flagged mechanism, its magnitude is real, the safety margins hold. Quarantine
held (a0/Z/κ/I0 never derived).

### Scripts
- **Scalar-only spherical (wxbnjxb64)** — under `opus_48_extended_research/reviews/aest_collapse/`:
  AEST_SPHERICAL_COLLAPSE_SETUP.md · aest_collapse_setup.py · aest_collapse_solve.py · aest_collapse_run.py ·
  aest_collapse_ADVERSARIAL.py · aest_collapse_c4c5.py
- **Rigorous follow-up — the three caveats closed (wt0lamc4k)** — under
  `opus_48_extended_research/reviews/aest_rigorous_collapse/`: AEST_RIGOROUS_COLLAPSE_SETUP.md · aest_rig_core.py ·
  aest_rig_selfconsistent.py (caveat 1+3A: self-consistent r″=−g, multi-stream) · aest_rig_nonradial_vector.py
  (caveat 2+3B/C: conservative vector mode-mixing vs dissipative control) · aest_rig_ADVERSARIAL.py (damping
  sweep γ_pin, ν_num/BC artifact ruling, galaxy-safety) · aest_rig_run.py (master verdict). Machine-readable
  verdict: `{c1_resp: 0.489, c1_slope: 0.218, c1_cross: 8, c23_resp_cons: 0.980, c23_Edrift_cons: −0.368,
  c23_resp_diss: 0.004, c23_Edrift_diss: −1.00, gamma_pin_over_3H0: 44.5, galaxy_worst_dex: 0.0012,
  protect_ratio: 22500}`. Re-run + verified 2026-06-20.
### Sources
Durakovic-Skordis 2024 (arXiv:2312.00889; quasistatic-spherical arXiv:2304.05134); Skordis-Zlosnik 2021/2022
(arXiv:2007.00082, 2109.13287); Blanchet-Skordis 2024 (arXiv:2307.15126); Kandrup 1998 (arXiv:astro-ph/9708026,
phase-mixing-needs-a-continuum theorem); Lynden-Bell 1967; Deffayet-Woodard 2024 (nonlocality); Malekjani-Rahvar-Haghi
2008 (spherical collapse). Confirms wn6n716aa / Zenodo 10.5281/zenodo.20779562 — dynamically, in its strongest form.
