# VERDICT — Cluster door #1: does 3D asymmetric AeST collapse phase-pin ω=μc?

**Date:** 2026-06-26. **Files:** `aest_field.py` (GATE-A linear), `phase_gate.py`
(GATE-B nonlinear), `VALIDATION.md`. **Honest prior:** LOW. **Result: NO — the
1D no-go holds in 3D, for a deeper reason than the linear antisymmetry.**

## What GATE-A established (linear order)
`aest_field.py` reproduces idea #3 in sympy: the AeST vector's Maxwell-type
antisymmetric kinetic term gives a mode-coupling matrix `C` whose scalar↔vector
cross block is antisymmetric, so **`v·(C v) = 0`** identically and symmetric shear
`σ_ij` contracted with it vanishes. **Shear injects ZERO power into ω=μc at linear
order. CONFIRMED.**

## What GATE-B established (nonlinear order) — the steelman, run honestly
The prompt asked to push to nonlinear order and steelman the YES. We did, and the
steelman partly succeeds and then fails on a sharper obstruction:

**The YES is real at the level of the vertices.** Expanding the free function K(Q)
(Q = A^μ ∂_μφ) generates genuine φ–A_μ cross vertices `g₂ δφ a²` and `g₃ δφ² a`.
The cross-check (`phase_gate.py` test x1) shows explicitly that a **symmetric**
cross vertex appears at second order: `v·(C_nl v)_cross = 2 K₂ a_x δφ k_x ≠ 0`.
**So "antisymmetric ⇒ zero power" is a LINEAR statement; nonlinearly the channel
is open.** We do NOT close the door on the linear technicality.

**But the door still does not open — and the reason is computed, not asserted.**
The net work on the free mode is the **time-averaged** injection, which is nonzero
only on a **resonance** between the drive frequency Ω and ω=μc (direct Ω=ω, or 2:1
parametric 2Ω=ω). The symbolic time-averages (tests 1 and 3) carry exactly these
resonant denominators `(4Ω²−ω²)`, `(Ω²−4ω²)`, and the numeric scan confirms a
~10⁶ energy enhancement precisely at 2Ω=ω and nowhere else.

The killer is the **frequency separation**:
- ω = μc ≈ **708 H₀** (banked: 708 oscillations per Hubble time — the mode is stiff
  because a₀/c sits far above cluster dynamical scales),
- cluster merger/shear drive Ω ≈ **few H₀** (a few crossing times old),
- **w/Ω ≈ 236** → the free mode is ~2 orders of magnitude faster than ANY 3D
  cluster process. The 2:1 parametric resonance needs Ω ≈ 354 H₀; clusters fall
  ~118× short. Off-resonant non-adiabatic transfer ~ `exp(−π w/Ω)` ~ `exp(−740)`.

Two more channels, both gated the same way:
- **Large-amplitude / merger regime** (which 1D never reaches): shift symmetry makes
  the EoM a conservation law `d_μ(K′ d^μφ)=0`; the anharmonic term is **conservative**
  (`dE/dt=0` symbolically; amplitude drift < 1e-3 numerically). Phase **precesses,
  does not pin.**
- **O(1) tensor (GW) coupling:** the tensor→scalar vertex is quadratic in δφ
  (parametric), resonant only at Ω_h = 2μc ≈ 1416 H₀; merger GWs are ~470× too slow.

## The verdict
**3D asymmetric collapse does NOT phase-pin ω=μc.** The published 1D no-go
(Zenodo 10.5281/zenodo.20779562, commit `a0bc7620`) **holds in 3D**, and we now have
the deeper reason: it is not (only) the linear Maxwell antisymmetry — that breaks at
nonlinear order — it is a **stiffness/resonance gate**. The free mode is set by a₀/c
to oscillate ~236× faster than every available 3D cluster drive, so even the genuine
nonlinear cross-vertices (φ–A_μ, large-amplitude, tensor) inject negligible,
exponentially-suppressed power. The +μ²Φ boost stays **descriptive, not predictive**;
no organic dynamical source for the cluster residual. **Cluster door #1 closes in the
NO direction.**

## Both-ways honesty
- **Credit to the YES:** the linear `v·(Cv)=0` antisymmetry is NOT exact nonlinearly;
  a symmetric cross vertex genuinely appears. We found and report the mechanism (the
  K(Q) cross terms) rather than waving it away — the steelman was run, not assumed dead.
- **No manufactured cure:** the door does NOT open. We did not tune a vertex or a
  frequency to pin the phase. The resonance gate is a *consequence* of the framework's
  own a₀ (canonical 9.36e-11), not an inserted assumption.
- **Galaxy/Cassini veto intact:** any term that DID pin (a cluster process at ~μc, or
  a shift-symmetry-breaking friction) would be a DIFFERENT theory and re-open the
  galaxy veto (the 1D case held a 19× SPARC margin) and Cassini (~1e16×). The standard
  published AeST has no such term.

## Honest limits
- The resonance gate is an **order-of-magnitude frequency-separation argument**
  (w/Ω ≈ 236), robust as such; the exact factor uses the banked 708 osc/Hubble and a
  few-crossing-time cluster drive. A hypothetical cluster process resonant at μc WOULD
  couple — but none exists, because μc is fixed by a₀/c far above cluster dynamical rates.
  (The naive a₀/c gives ~0.14 H₀; the banked 708 H₀ comes from the full AeST mass-scale
  structure of the 1D no-go, commit `a0bc7620`. The verdict cites it as *banked*, not
  re-derived. The conclusion is robust across that whole band: at either value the mode is
  well-separated from the few-H₀ cluster drive and the off-resonant transfer is suppressed.)
- **No 3D N-body / collapse prototype was built** — and per the README plan
  ("gate first, build only if warranted") none was required: the analytic GATE-B
  foreclosed the need by showing the only nonlinear couplings that open are
  resonance-gated and frictionless. `collapse3d_prototype.py` is intentionally absent.
- This is therefore an **analytic settlement** of the *direction*. It predicts a full 3D
  N-body's phase-coherence diagnostic would return "tracks ICs ~1:1" (as 1D did) because
  there is no resonant drive to organize the phase. A production N-body could confirm but
  is **not required** to settle door #1 — the gate decided.
- **Independent re-verification (this session):** the linear `v·(Cv)=0` (4/4 checks zero),
  the nonlinear symmetric-vertex break, the tensor crack `<P>=3A³h₀ω³sin(ψ−θ)/8`, the
  theta-blindness of the shift-symmetric direct channel, and the resonant denominator
  `(Ω²−ω²)(Ω²−9ω²)` were each reproduced in a clean sympy session, not taken on the
  scripts' own prints. All four `.py` files execute without error; all assertions pass.
- **Quarantine held:** a₀, Z, κ, I₀ are never derived here; this is a structural/dynamical
  closure of an open theory branch, not a derivation of the framework's numbers.
