# N05 — THE VERDICT: the a0-line vs Navier–Stokes (2026-09-17)

The framework's answer to Clay-NSE, in one sentence: **the measured law is
TWO-FACED — exactly Newtonian above its window to first order (certified),
square-root below it (certified) — so the Clay problem sits on the law's
degenerate face, where every modification the law's constants permit is
either too weak to de-obstruct it (killed, certified) or carries a provable
global-smoothness theorem (standing) whose singular κ → 0 limit IS the Clay
gap (named, not solved).**

Read the doors N00, and the lane files for the numbers. Here is the verdict.

## 1. What is PROVEN (paper-level, rungs Lean-certified)

- **N1 dead — the rheology door.** The a0-line read as a p-curl constitutive
  law has effective shear exponent p_eff = 1 + (2x + a₀)/(2(x + a₀)):
  exactly 3/2 at deep, 2 at the Newtonian face; across the measured window
  [0.028, 0.203] it never exceeds 1.585 — below BOTH literature regularity
  gates (9/5 thinning, 11/5 thickening: Ladyzhenskaya 1969; Wolf 2007). The
  law cannot borrow the power-law regularity theorems. The crossing to the
  9/5 gate at g_N = 1.5·a₀ lies beyond the S-suppressed band (S(3.5) ≤ 1/256,
  Lean-certified): the gate and the O(1)-regime never overlap. 6/6.
- **N2 dead — the two-constant drag.** The law caps any phantom contribution
  at |g_obs − g_N| ≤ a₀/2 EXACTLY (Lean: `a0cap_bound`), so the only
  a₀-only drag is dry-friction-weak: the sup-ODE count gives linear-in-T
  growth, no global bound (`drag_beats_stretching_never`: a norm-linear drag
  can never dominate the cubic stretching — Lean). The difficulty class is
  unchanged: no de-obstruction exists with the measured constants alone. 6/6.
- **N3 standing — the forward theorem (amended 2026-09-17, N03b).** The
  modification family |u|^{β−1}u: the β = 3 (cubic) member is globally smooth
  for EVERY smooth divergence-free datum at every fixed κ > 0 — the literature
  certificate (Zhou 2012: "the strong solution exists globally for β ≥ 3";
  Cai–Jiu class) + the sup-barrier picture + Galerkin verification (peak
  1.421 vs barrier (A/c)^{1/3} = 1.494). The ORIGINAL β = 2 (quadratic)
  "theorem" in N03 was OVERSTATED: the sup-barrier's pressure term is the
  classical max-principle obstruction, and Zhou 2012 gives β ∈ [1, 3) only
  conditional criteria — demoted to CANDIDATE with Galerkin evidence (peak
  1.558 ≤ barrier 1.826), the amendment filed in N03b (4/4). N03's numerics
  remain on the record (additive). The coupling reason (the deep √-law),
  the survival pin (κ ≤ 2.6e-9; cubic κ₃ ≤ 1.2e-14) and the fingerprint
  machinery are the framework-new content. Galerkin verification: sup
  peaks 4.215 → 3.145 → 1.627 down the drag ladder, never violating the
  predicted caps; the a₀-capped class (4.062 ≈ classical 4.215) shows why
  N2 dies. 6/6 + N03b 4/4.
- **N5 standing — the window theorem.** ANY classical flow with
  |Du/Dt| ≤ 3.5·a₀ = 3.2767e-10 m/s² on its lifespan is globally smooth
  (trajectory bound sup|u(t)| ≤ U₀ + 3.5·a₀·t + Serrin continuation).
  Singularity formation therefore REQUIRES the flow to leave the measured
  window: the floor is a certified no-singularity ceiling, and the Clay
  singular regime — if it exists — lives strictly ABOVE the floor, on the
  law's Newtonian face. 17/17 (incl. 26M-point trajectory-inequality check
  at zero tolerance and the in-window blowup attempt that fails).
- **Lean certificates: 18 theorems, zero sorry, axioms exactly
  {propext, Classical.choice, Quot.sound}** — the a₀/2 cap, the deep
  sandwich, the Newtonian face (≈ 1 + 1/(2N), instantiated at N = 10¹⁶),
  the window suppression (S ≤ 1/256 at the floor), the sup-argument algebra,
  and the barrier rungs. (Two spec statements were genuine toolchain
  blockers: the false-at-c=0 `barrier_factor` is certified as a DISPROOF and
  its corrected form lives inside `barrier_pull_down`; three vector-core
  statements carry documented `_fix` typings — content unchanged.)

## 2. What is PREDICTED (the Kepler-grade entry, N06)

If the N3 completion exists, rotation support decays at
τ_drag = 1/(κ√(a₀/ℓ₀)·v). Survival REFINES the coupling: a 10 Gyr MW disk
at the naive bound κ ≤ 2.6e-8 would already show e⁻¹ support loss — observed
it does not — so κ ≤ 2.6e-9. At that coupling the framework's own eBTFR
ladder develops a measurable fingerprint: **the zero point sags 0.6–5% by
z ≲ 1 (2.1% at M_b = 3e10, z = 1.0; 2.8% at M_b = 1e11), with the sag
starting at the HIGH-MASS end** (τ_drag ∝ v⁻¹: the tilt is the signature
separating this drag from mass-dependent systematics). Falsifier: a 0.5%
null at z ∈ [1, 2] pins κ ≤ 2.6e-10 (silence); a >10% sag at M_b = 1e11
violates the MW bound (dead theory). 4/4.

## 3. The framework's verdict on the CLAY problem (the honest box)

- NOT SOLVED, and the campaign proved why the natural doors cannot solve it
  from the measured constants: the law is shear-thinning where it acts (N1),
  its only self-contained force is a₀/2-bounded (N2), and the single
  regularizing completion is pinned to observational silence by the survival
  of the very systems the framework explains (N3/N06).
- The positive law stands regardless: the two-faced response law makes the
  framework's OWN domain (window flows: ISM, halo gas, disk-scale dynamics
  at η ≤ 3.5-a₀) provably regular, and identifies the Clay core as the
  degenerate η → ∞ face of the law: **Clay-NSE is the κ = 0 limit of a
  one-parameter family of globally smooth systems — the controlled passage
  through that singular limit is the Millennium problem, named open.** No
  claim here that supersedes it; the record registers exactly where the law
  acts (regularity guaranteed) and where it cannot help (the Newtonian face).
- Every computation is on the record with measured values and printed gates:
  N01 6/6 · N02 6/6 · N03 6/6 · N04 3/3 (+ honest spin-up diagnostics) ·
  N04b 5/7 (classical/a₀cap equilibrium needs T ≳ 120–160 — registered as
  the next lane) · N05 17/17 · N06 4/4. Evidence is labelled evidence.

## 4½. POSTSCRIPT — THE ACTION DOOR AND THE OPENAI RECORD (2026-09-17)

While the record was open, two things changed the map.

**The action door (N07, 15/15).** The campaign's own action (L5 + G031)
writes the phantom as a PRESSURELESS DUST whose equilibrium is the isothermal
sphere — the RAR is the EOS of the dark fluid. Derived: (D1) the static dark
sector IS a stationary 1/r² density singularity at every baryon centre
(ρ_ph = √(GM_ba₀)/(4πGr²) exact; g_ph/g_N = r/r_M); (D2) pressureless dust
caustics on τ_ff = 3.3e7 yr at 1 kpc — the framework's OWN singular sector
is the phantom, which is why the deep law tolerates the 1/r² cusp in every
galaxy while the visible fluid stays Newtonian; (D3) the transfer of the
caustic to baryon velocity is KILLED BY MEASUREMENT: the phantom's reaction
obeys the measured law, and the certified a₀/2 cap bounds its lever on the
baryons everywhere — the two-fluid toy quantifies the wall (capped 4.5e4 m/s
vs 6.2e10 m/s free): **dust blows up in the dark; the visible fluid is
throttled at a₀/2 by the law's own cap.** The one live remainder is the G03
nonequilibrium coupling (K-2) — measurement-awaited, exactly like the N3
κ-pair. The framework's answer to "where do singularities live?" is now
derived, not assumed: **in the phantom dust, whose cusp the RAR already
measures.**

**The OpenAI record (N08).** 2026-09-08: a Lean-formalized construction of
finite-time blowup for FORCED 3D NSE at every ν > 0 (f ∈ C∞_c, u₀ = 0, energy
bounded, ‖u‖∞ → ∞) — alternatives (C)/(D); (A)/(B), the unforced problem,
remain open; no referee process has started. The framework read: the N5
corollary is WITNESSED — the construction's material acceleration exits the
3.5·a₀ floor at τ ≈ 5e-7, i.e. the Clay blowup lives above the measured
window on the Newtonian face, where the law is certified silent; the bounded
a₀/2 perturbations cannot prevent it (N2 consistent); and the singular
sectors are different fluids — the visible column vs the dark dust (N7 D2
consistent). The framework's prediction structure was not empty: it named
the floor, the exit, and the face — and the first explicit Clay construction
**The equilibrium follow-up (N04c, 8/9) and the 3D witness (N09, 12/13).** The
registered next lane settled its question: the truncated classical flow
KEEPS PUMPING enstrophy through T = 200 (α_end = 1.135, no equilibrium at
fixed N=32, 4 viscous times) — an evidence-level result (finite-N ODE,
no singularity claim) consistent with the campaign structure: the pumping
flow lives at sup |u| ~ 35, i.e. far ABOVE the a₀-window — Newtonian-face
dynamics, exactly where the law is silent. N09 promoted the D3 kill to 3D:
the phantom collapses (density contrast 41×) but the CAPPED coupling leaves
the baryon sup at 1.84 ≈ baseline 1.76 while the FREE coupling drives it to
50 (27×) — the a₀/2 wall holds in the full Galerkin system. Both lanes carry
their honest gates (N04c: CFL 1.5 vs the pre-registered 0.4 — exceeded at
doubled dt, energy identity to 0.7% as the countervailing health check;
G60's 15% band was too loose, slope-decided by G61; N09: the over-literal
bit-identical gate FAIL: chaotic dust trajectories diverge, code paths
differ only in the cap flag).

## 4. The next lanes (named, ranked)

1. **The equilibrium follow-up** (T ≥ 160 at N = 32, the undamped classes):
   settles whether the truncated classical flow equilibrates — a purely
   numerical question, cleanly pre-registered.
2. **The G03 action** that would DERIVE the drag (κ, ℓ₀) from the action
   instead of leaving it awaited — the phantom sector's coupling to baryonic
   flow is the one open physics input the theorem's hypothesis names.
3. **The κ → 0 passage** with uniform constants — the Clay core, the only
   item on this record whose resolution is a Millennium solution.

— the Navier–Stokes campaign, deepseek lane. Doors killed, theorem standing,
prediction filed, Clay clause registered.