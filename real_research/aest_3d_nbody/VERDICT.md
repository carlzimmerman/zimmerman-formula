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

## NUMERICAL CONFIRMATION (2026-06-26) — the prototype the analytic gate said wasn't required, built and run anyway

The earlier "Honest limits" said no 3D prototype was built because the gate foreclosed
the need. Carl/Gemini asked for it anyway, as a numerical backstop. It is now built
(`collapse3d_prototype.py`), gated (`validate_prototype.py` → `VALIDATION_PROTOTYPE.md`),
and **independently re-run + adversarially audited this session**.

**VERDICT: (A) CONFIRMED.** The 3D shear-injection prototype numerically reproduces NO-PIN.
The analytic gate is now numerically backstopped. Cluster door #1 is settled analytically
**and** numerically, in the **NO** direction.

### What the numerics show (reproducible: `python3 validate_prototype.py`)
- **Headline adversarial trial** (N=28³, stiff ω=708 H₀, full non-radial 3D shear σ_ij +
  O(1) tensor drive at cluster Ω≈3 H₀): scalar-phase **circ-std stays O(1), 1.865→1.977 rad**
  (does NOT shrink toward 0), **IC-lock = 0.961** (phase tracks ICs ~1:1). The mode energy
  is **pumped/oscillatory (+1.4e-2), not bled out** — confirming the no-friction theorem
  (shear is a conservative parametric pump, not a dissipative drag).
- **All three validation gates PASS:** (i) spherical/1D limit reproduces the no-go
  (random-IC circ-std 1.98–2.05, IC-lock 0.977; uniform-IC breather stays 0.00–0.02);
  (ii) a₀=9.36e-11 quarantined input, the stiff ω inherited (not tuned) — well-separated
  from the few-H₀ cluster drive at both the naive 0.14 H₀ and banked 708 H₀ bands;
  (iii) symplectic energy drift −2.2e-4, bounded/non-secular, no numerical friction.
- **Diagnostic is provably ALIVE, two independent ways (not dead-rigged):**
  (1) the adversarial control driving ON the 2:1 Mathieu parametric resonance (Ω_h=2ω=1416)
  pumps the mode by **~16 orders** (ratio 1.22e16) and stays dark off-resonance — it
  responds hard *only* when resonant, which is *why* the off-resonant few-H₀ cluster drive
  can't pin a stiff ω=708 mode; (2) **forcing a real synchronization mechanism into the full
  evolve+diagnose pipeline drives circ-std 1.70 → 0.0000** (re-verified this session) — a
  genuine pin WOULD surface. A positive-control Rayleigh friction −γπ bled **−95%** of the
  energy, so the pipeline shows dissipation if present. The AeST run does not pin because
  the physics does not pin, not because the metric is floored.

### Audit caveats — kept honest, do not overstate the numerics' reach
The numerical backstop is **genuine but scoped**. Two limits, independently re-confirmed:
- **The named non-radial shear contributes ~nothing to the phase diagnostic** (Δcirc-std
  ~1e-10 shear-only vs no-drive; the vector moves ~3.6e-5 of its magnitude). The active
  symmetry-breaker in the headline run is the **tensor h_ij parametric channel**, not the
  σ_ij shear the writeup foregrounds. The perturbation is real (scalar perturbed at the
  100% level) but it is the tensor pump.
- **The nonlinear K(Q) cross-vertices g₂,g₃ are numerically dormant** in the headline run:
  g₂=g₃=0 vs g₂=g₃=50 changes circ-std by ~2e-5 (they sit ~1e-5 below the stiff ω²φ term).
  So the numerics rigorously confirm **only the LINEAR stiff-mode + off-resonant parametric
  no-pin**, plus the sharp 2:1 resonance structure. **The genuine NONLINEAR no-pin still
  rests on the analytic resonant_channel.py argument** (the symmetric cross vertex
  ⟨P⟩=(3/8)A³h₀ω³sin(ψ−θ), resonance-gated + frictionless). The prototype confirms the
  gate's *direction* and its *mechanism* (stiffness + no friction), not the full nonlinear
  vertex algebra — that remains analytic. Audit verdict: **genuine-confirms-gate.**
- The gate (i) target was reframed from the published 1D "circ-std ≈ 1.34" to an
  **O(1) + IC-lock>0.8** criterion (3D uniform-random ceiling is ~2.7, not 1.34). The
  no-go is reproduced in spirit (phase tracks ICs ~1:1, no organization to 0), not at the
  specific 1.34 number.

### Both-ways honesty (the premise correction)
- **The prompt's "friction" premise was wrong, and we say so.** The framing imagined shear
  as a dissipative friction that could lock the phase. It is not: the shift-symmetric AeST
  action is **conservative**, so shear is a **parametric pump** — it can move amplitude
  (and does, on resonance) but has **no phase fixed point**. Pinning would require
  irreversible friction, which AeST has at no order. The numerics show exactly this:
  energy pumps, phase precesses/librates, never relaxes-and-locks.
- **No manufactured re-opening, no high-priesting.** The door does not re-open: the
  numerics confirm the settled NO. Nor did we floor the diagnostic to force a NO — it is
  alive (forced sync → 0). This is a clean backstop of a result that was already
  analytically settled, with the honest caveat that the *nonlinear* leg stays analytic.
- **Quarantine held:** a₀, Z, κ, I₀ remain INPUT, never derived. This confirms a
  structural/dynamical NO-pin; it derives none of the framework's numbers.

**Files:** `collapse3d_prototype.py` (the 3D field evolution + shear/tensor injection +
phase diagnostic), `validate_prototype.py` (gates + adversarial resonance control),
`VALIDATION_PROTOTYPE.md` (auto-generated live-number gate report).
