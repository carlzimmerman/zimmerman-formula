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

## (5) Honest caveats (both-ways — the skeptic's catches, recorded straight)
- **MAIN WEAKNESS:** the matter collapse is a **KINEMATIC PROXY** — `aest_collapse_solve.py` lines 311–324
  prescribe r_phys via a cosine-contract formula; r″=−g_AeST is never time-integrated (despite the line-309
  comment). This caps rigor but does **not** flip the verdict (the phase result is *source-independent* — a
  statement about the conservative homogeneous mode, with the real AeST field + real KG wave; only the
  density *history* is a proxy).
- The 1+1D reduction drops the AeST **vector-mode E coupling** (SZ2021 Eq 12) and K_B sector — the most
  plausible (still unlikely) place a friction term could hide.
- Robustness blemishes: Hernquist + galaxy-slope return NaN; the static [−22, +22] span is a scan-width
  artifact (physical [−3.12, +3.97]); the nonlocality theorem was mis-cited (it is **Deffayet & Woodard
  2024**, not Blanchet-Marleau-Skordis).
- **Scope:** a full 3D cosmological AeST N-body is still needed to settle it *definitively* (adding
  self-consistent collapse, the vector/tidal channels, and a genuine cosmological χ(t) outer boundary) — but
  the spherical reduction points **firmly** at the no-go because the obstruction is structural, so a reversal
  is unlikely.

## Net
The cluster door does **not** reopen as the strong predictive result. The +μ²Φ boost is real (~10⁵× the
naive coupling) and galaxy+Cassini-safe, but **descriptive, not predictive**, in the static *and* dynamical
cases. The published no-go (Zenodo 10.5281/zenodo.20779562) stands, now confirmed in time. Credit held: the
+μ² lever is the authors' own flagged mechanism, its magnitude is real, the safety margins hold. Quarantine
held (a0/Z/κ/I0 never derived).

### Scripts (under opus_48_extended_research/reviews/aest_collapse/)
AEST_SPHERICAL_COLLAPSE_SETUP.md · aest_collapse_setup.py · aest_collapse_solve.py · aest_collapse_run.py ·
aest_collapse_ADVERSARIAL.py · aest_collapse_c4c5.py
### Sources
Durakovic-Skordis 2024 (arXiv:2312.00889); Skordis-Zlosnik 2021/2022; Blanchet-Skordis 2024; Deffayet-Woodard
2024 (nonlocality); Malekjani-Rahvar-Haghi 2008 (spherical collapse). Confirms wn6n716aa / Zenodo 10.5281/zenodo.20779562.
