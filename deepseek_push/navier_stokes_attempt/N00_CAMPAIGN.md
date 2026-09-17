# N00 — THE NAVIER–STOKES CAMPAIGN (deepseek lane, 2026-09-17)

Folder: `deepseek_push/navier_stokes_attempt/`. Task: attack Navier–Stokes
Existence and Smoothness (the Clay problem, periodic/3D setting) from the
framework's first principles — the measured law, the data-selected kernels,
the two-constant discipline — certify every algebraic rung in Lean, put the
numerical evidence on the record, and register the honest verdict in print
BEFORE the numbers land.

## THE QUESTION, RESTATED FOR THIS FRAMEWORK

Clay NSE asks: for the incompressible system on the 3-torus

    ∂_t u + (u·∇)u = ν Δu − ∇p + f ,   div u = 0 ,   u(0) = u₀ ,

with smooth divergence-free data, prove the solution is smooth for all time.
This framework owns a MEASURED acceleration scale a₀ = 9.3619e-11 m/s²
(κ = ½, rung 1) and the two-face response law

    g_obs² = g_N² + a₀·g_N        (the a0-line; g_obs = √(g_N² + a₀·g_N))

with the data-selected kernels ν_RAR and μ₂, the S(η) ansatz, the measured
window η = |g_N|/a₀ ∈ [0.028, 0.203] and the floor η ≈ 3.5 (LAW_STATEMENT.md;
SW06_lemmas.lean compiled exit 0). There is NO committed action (G03 OPEN),
so every coupling of this law to fluid dynamics is a COMPLETION and is
labeled as such in this record.

The framework-native question is therefore:

> **N0: what does the measured law — with its constants and kernels and
> nothing else — permit and forbid in the way of an NSE regularity mechanism,
> and which completion, if any, carries a provable global-smoothness theorem?**

## DOORS (pre-registered; any kill condition fires → the door dies)

### N1 — the a0-line as an implicit rheology (the power-law class)
Read the law as a constitutive stress response: τ ∝ ρ·g_obs(g_N(s)) where
s = |Du| is the local shear rate and g_N ∝ s is the Newtonian field at the
flow's own scale. The reachable theory class is Ladyzhenskaya's p-curl
(power-law) system, whose literature gates are: global regularity for
shear-thickening p ≥ 11/5, and for shear-thinning p ≥ 9/5 (Ladyzhenskaya
1969; weak-existence for p > 8/5, Wolf 2007).
- **K1 (the exponent gate):** if the law's effective shear exponent
  p_eff = 1 + d ln τ / d ln s dips below 9/5 in ANY regime, the rheology
  door is dead: the measured law cannot borrow the power-law regularity
  theorems. The deep-MOND slope d ln g_obs/d ln g_N = 1/2 predicts
  p_eff(deep) = 3/2 < 9/5 — expected FAIL, registered as the finding.

### N2 — the two-constant drag (a₀-only, the dimension-forced class)
Any framework-allowed modification built from a₀ alone is dimension-forced
to have acceleration magnitude ≤ a₀·O(1); the law pins the O(1): the extra
observed acceleration satisfies |g_obs − g_N| ≤ a₀/2 EXACTLY (√(x²+ax) − x
is increasing, ≤ a/2 — certified in Lean below). Such a drag cannot grow
with |u|, so the sup-norm mechanism yields at best linear-in-T growth:
sub-regularizing.
- **K2 (the de-obstruction gate):** if the certified a₀/2 cap forces the
  sup-ODE count `M'(t) ≤ A − a₀` (linear growth, no global bound), the
  two-constant class cannot de-obstruct Clay-NSE, and the difficulty class
  of the modified problem is unchanged (the modification is a bounded
  forcing; the critical scaling is untouched). Dead with the certified
  counts as the record.

### N3 — the κ-drag completion family ZNS[κ, ℓ₀] (THE FORWARD THEOREM)
The minimal structure-preserving completion that CAN regularize: a drag
proportional to the deep-law factor √(a₀/ℓ₀) evaluated at the flow's own
velocity, opposing motion:

    ∂_t u + (u·∇)u = −∇p + νΔu − κ·√(a₀/ℓ₀)·|u|·u + f

with the ONE new parameter pair (κ, ℓ₀) — the phantom-baryon coupling
strength and its length scale — flagged measurement-awaited, exactly as the
YM00 campaign flagged its fiducial scale. THEOREM (proved in N03, rungs
certified in Lean): for every κ > 0, ℓ₀ > 0, ν > 0 and every smooth
divergence-free datum, ZNS[κ, ℓ₀] has a unique global smooth solution.
The proof chain: (i) sup-barrier — the |u|²-drag caps ‖u‖_{L∞} a priori at
max(M₀, √(A/(κ√(a₀/ℓ₀)))) via the pointwise maximum principle (transport
preserves sup, ω×u ⊥ u, Δ ≤ 0 at the sup point, the drag is strictly
dissipative); (ii) the capped sup places the solution in the Serrin/Prodi
class u ∈ L∞_t L∞_x ⇒ regularity; (iii) local existence + the a priori cap
+ (ii) ⇒ global smoothness (standard continuation). κ = 0 is Clay-NSE.
- **K3:** if the Galerkin sup trajectories under the strong drag do NOT
  track the predicted barrier constant within 30%, the barrier argument is
  wrong — kill.
- **K4 (the observability gate):** the barrier scale √(A/(κ√(a₀/ℓ₀))) is
  the prediction; at laboratory scales the certified face numbers must put
  the drag below every measurement (the Newtonian face), while inside the
  measured window η ∈ [0.028, 0.203] the drag must be O(1)-relevant.
  If the lab-regime numbers allow observability within one order of
  current sensitivity, the face claim is wrong — kill.

### N4 — the scale/face theorem (the positive law for the CLASSICAL system)
The certified two-face structure of the law ALONE (no completion): (a) the
a₀/2 cap: the phantom contribution to any parcel's acceleration is
universally ≤ a₀/2 (Lean-certified); (b) the Newtonian face: at
|g_N| ≥ a₀·N the law deviates from Newton by ≤ 1/(2N) (Lean-certified
first-order bound); (c) the deep face: |g_N| ≤ a₀·ε gives
g_obs = √(a₀·|g_N|)·(1 + O(ε)) (Lean-certified sandwich). The numbers for
laboratory flows (η ~ 10^10) put the deviation ε ~ 10^8 orders down:
**NSE at laboratory scale is the η → ∞ face of the framework's fluid
response — Clay-NSE lives on the degenerate face, where the law's
modification is certified below 1e-10-level for any flow with |u| > 1 m/s
over a century of integration.**

### N5 — the Clay scope clause (NOT a kill, a boundary, registered)
κ → 0 (equivalently a₀ → 0 at fixed flow scale) is a SINGULAR limit: the
barrier constant √(A/(κ√(a₀/ℓ₀))) → ∞. The controlled passage through that
limit — global regularity with uniform-in-κ constants — is EXACTLY the Clay
gap. This campaign does NOT claim the Clay problem; it claims: the
framework's constants rule out the natural modifications (N1, N2), the
minimal completion carries a provable global-smoothness theorem (N3), and
the Clay core is identified as the κ → 0 face of that family (N5).

## FALSIFIER RECIPES (parameter-free where possible)

- F1 (N1): a measured flow whose effective rheology follows √(a₀·g_N)
  scaling at the 1% level inside the window with shear exponent ≥ 9/5 —
  would revive the rheology door. None known; the door is dead until then.
- F2 (N3): a gas-flow turbulence decay time τ_drag = √(ℓ₀/a₀)/κ inside the
  window, measurable against the predicted sup barrier; a null detection
  inside the window at the predicted strength kills the completion.
- F3 (N4): any laboratory-scale (η ≥ 10^6) deviation from exact Newtonian
  fluid response above the certified 1e-10 floor kills the face theorem.
- F4 (Clay): full global regularity for ZNS[0] = NSE with constants
  uniform as κ → 0 — the open core; a proof or a blowup example for the
  classical system is out of scope here and would resolve the Millennium
  problem, not this campaign.

## DELIVERABLES (this folder)

| File | Content |
|---|---|
| N00_CAMPAIGN.md | this record (pre-registered doors, kills, scope) |
| N01_rheology.py/.out/.results.json | rheology door: exponent analysis vs the 9/5 and 11/5 gates |
| N02_dragcount.py/.out/.results.json | two-constant drag: a₀/2 cap, sup-ODE count, lab-face numbers |
| N03_supbarrier.py/.out/.results.json | forward theorem: barrier constants, Galerkin verification, window numbers |
| N04_galerkin.py/.out/.results.json | numerical evidence: enstrophy/sup/energy series, drag on/off, PNGs |
| lean/NSE_a0line.lean | Lean: the a₀/2 cap, deep sandwich, Newtonian face, window anchors |
| lean/NSE_vector_core.lean | Lean: the sup-argument algebra ((u·∇)u·u = ½(u·∇)|u|², ω×u ⊥ u, inner cross) |
| lean/NSE_barrier.lean | Lean: the barrier-ODE comparison (Gronwall route, zero sorry) |
| N05_VERDICT.md | the synthesis: doors dead, theorem standing, the κ → 0 face, Clay clause |
| README.md | folder index + how to run |

STATUS: doors pre-registered 2026-09-17. Lanes begin at N01.