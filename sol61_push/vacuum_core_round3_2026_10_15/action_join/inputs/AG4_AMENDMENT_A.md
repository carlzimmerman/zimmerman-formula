# AG4 — FROZEN CRITERIA AMENDMENT A (committed BEFORE the first derivation run; design-stage)

**Why:** calibrating G4 before running shows the uniform "< 1% for r ≥ 10 r_s" threshold is
only meaningful in the weak-stiffness regime (L* ≪ r_M). In the corner L* ~ r_M (e.g.
L* = 1 kpc upper bound with a dwarf r_M = 1 kpc) the screening radius r_s = L*²/r_M ~ r_M and
the stiffness term is galactic-scale BY CONSTRUCTION — γ=0 cannot be certified there at any
fixed multiple of r_s (hand estimate: ratio ≈ (L*²/2r²)(a₀/u−1) ≈ 4.5% at r = 10 r_M). A
hard <1% gate there would fail on a design miscalibration, not on physics. Legitimacy: no
run has executed; the original file stays unmodified (append-only).

## G4 as amended (pre-run)

- **G4-i:** L* = 5.75 pc corners (both r_M): ratio < 1e-6 for r ≥ 10 r_s. PASS/FAIL.
- **G4-ii:** L*/r_M ≤ 0.1 corners: ratio < 1% for r ≥ 10 r_s. PASS/FAIL.
- **G4-iii:** L*/r_M = 1 corner: NO hard threshold. Report the ratio profile and the radius
  r_1% where the ratio falls below 1% (expected ~ tens of r_M). The γ=0 reduction is then
  valid for the AG3 annulus regime only where r ≥ r_1%; recorded per corner, loud.
- G4 gate = G4-i ∧ G4-ii, with G4-iii reported. If G4-iii's r_1% intrudes on the AG3
  band regime (r ~ 1–3 r_M) for the L*=1 kpc bound, the AG3 B2 "stable" conclusion gets
  a stiffness caveat in the AG4 handoff (it does not change AG3's measured widths).

**Additionally (strengthens G1, no gate semantics changed):** the variational check must
build W_rem(u) explicitly as the antiderivative of the frozen K W_rem′(u) = u²/(a₀−nu)
(capacity-n family; at n=1 this is the ArgonClues-certified
K W_rem = a₀²(−ln(1−u/a₀) − u/a₀ − u²/(2a₀²)) up to a constant), and derive BOTH field
equations by jet-total-derivative Euler–Lagrange of the full radial action density — no
hard-coded W′ term. G1 passes only if the EL residuals against the physics forms
(div A = K ρ_b; A − (u²/(a₀−nu))P̂ + γ∇²P = 0) are identically zero.

Everything else in FROZEN_CRITERIA.md (93e579ec1) stands unchanged.
