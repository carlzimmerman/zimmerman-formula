# Validation gates — 3D AeST phase-pinning analytic gate

These are the gates the analytic GATE-A/GATE-B code must pass to be trusted. All pass.

## G1 — Linear antisymmetry reproduces idea #3 (`aest_field.py`)
The 4×4 mode-coupling matrix `C` on `v=(δφ, a_x, a_y, a_z)` has, at linear order,
a purely **antisymmetric** scalar↔vector cross block (Maxwell `F = dA`), so:
- `v·(C_anti v) = 0` identically (sympy),
- the scalar↔vector **cross power = 0** (sympy),
- `σ_ij A_ij = 0` (symmetric shear contracted with the antisymmetric coupling).

**PASS** — reproduces `GEMINI_AS_PLUS_CLUSTER_IDEAS_VERDICT` idea #3 (`v·(Cv)=0`,
Maxwell `|E|²−|B|²` antisymmetric coupling) in sympy. Shear injects zero power into
ω=μc at linear order.

## G2 — Reduce to the 1D no-go (`phase_gate.py`, test 2)
In the spherical / small-amplitude limit the shift-symmetric scalar EoM is a
conservation law `d_μ(K′ d^μφ)=0`; the homogeneous reduction conserves `K′ φ̇` →
the free mode is undamped. This is exactly the published 1D result (commit
`a0bc7620`: 708 osc/Hubble, no friction, collapse tracks ICs ~1:1).
- `dE/dt` on-shell `= 0` (sympy, conservative anharmonic),
- numeric amplitude drift over 200 periods `< 1e-3` at ε=0, 0.5.

**PASS** — the analytic gate reproduces the 1D no-go's no-friction core.

## G3 — Resonance gate is real, not assumed (`phase_gate.py`, numeric scan)
Direct numerical integration of a stiff KG oscillator (ω=708 H₀) driven through the
nonlinear cross vertex `g₂ δφ a²` by a source `a(t)~cos(Ω t)`:

| drive Ω (H₀) | w/Ω | max KG energy |
|---|---|---|
| 3 (cluster) | 236 | 4.0e-6 |
| 50 | 14 | 4.1e-6 |
| **354 (2:1 resonance)** | **2** | **5.9e0** |
| 708 | 1 | 1.0e-6 |
| 1416 | 0.5 | 1.0e-6 |

Resonant/cluster energy ratio ≈ **1.5e6** (~6 orders). The door opens only at the
2:1 parametric resonance 2Ω=ω; the cluster drive is ~118× below it.

**PASS** — the resonance gate is computed, not asserted. The symbolic resonant
denominators `(4Ω²−ω²)`, `(Ω²−4ω²)` in tests 1 and 3 match the numeric peak.

## G4 — Deep-MOND / a₀ scale consistency
The free-mode frequency ω=μc is set by the AeST mass scale tied to a₀=9.36e-11.
Banked: 708 oscillations per Hubble time → ω ≈ 708 H₀. Cluster dynamical rates are
a few × H₀ (clusters are a few crossing times old). The frequency separation
w/Ω ≈ 236 is therefore a **physical** consequence of a₀/c being far above cluster
dynamical scales, not a tuned input.

**PASS** — the stiffness is inherited from the framework's own a₀, at the canonical
value, with no free knob.
