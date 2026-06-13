# agentMM — Route C: FOLIATION / CONFORMAL-ANOMALY

**Question.** Does the foliation-breaking of dS invariance — through (i) the conformal anomaly
under the preferred slicing, or (ii) the modular/Tomita-Takesaki structure of the edge state —
FORCE a specific edge measure ρ(b) at b → c_χ? Or is the anomaly silent on the family edge?

Coefficient quarantine ABSOLUTE: ζ̃ and (16π/3)^(1/4) are INPUT, never re-derived. All pure
numbers RAW. Both-ways hostility: a "silent" verdict is verified as hard as a "forces" verdict.

## Inputs pinned (from agentEE STEPs 1-2, read this run)
- Foliation breaks SO(4,1) → residual **E(3) ⋊ dilatation** (7-param). Dilatation acts as
  proper-time translation on comoving worldlines ⟹ worldline pullback STATIONARY.
- Conformal (c_s=1) member: **KMS at H/2π**. Free b-family member: KMS at κ/2π,
  κ = H/√(1−b²/c_χ²)-type, with κ²=a²+H² at c_χ=1; b = a/κ.
- Worldline density diagonalizes in the **Mellin variable of dilatation**:
  W(τ)=(1/2π)∫dν |φ̃(ν)|² e^{−iνκτ}, ρ̃(ω)=(H²/4π²c_χκ)|φ̃(ω/κ)|² ≥ 0.
- Free member spectral density = Planck: ρ̃_free(ω) ∝ ω/(1−e^{−2πω/κ}).
- The EDGE in question: b → c_χ, where κ(b) = H/√(c_χ(c_χ²−b²)) → ∞ (the luminal edge of
  the Deser-Levin family). u = 2π/κ ~ √(c_χ−b) → 0.

## What "the anomaly forces ρ(b)" would have to mean
ρ(b) is a measure over the family label b (worldline velocity rel. khronon frame), NOT over the
mode/scale label. The conformal anomaly and the modular flow are objects attached to the STATE /
the slicing. For Route C to be non-silent, one of these state-side objects must pick out a
preferred WEIGHT in b near b=c_χ. Begin computing whether either does.

## STEP C1 — The conformal anomaly density carries NO family label (machine)
On the FIXED dS + comoving-khronon background the anomaly-eligible local scalars are all pure
H-powers (R=12H², R_mn n^m n^n=3H², K=3H, K_mnK^mn=3H², a²=0 — comoving foliation geodesic).
**None carries b.** The trace anomaly ⟨T⟩ = cW²−aE₄(+b□R), built from these, is a constant
field; it is the SAME at every spacetime point and along every worldline. The family label b is a
PROBE-worldline label; the anomaly is a property of the condensate/background, which b does not
change. ⟹ The conformal anomaly **cannot** be a function of b, hence cannot weight ρ(b).
Machine: /tmp/agentMM_C1.py, all scalars b-free.

## STEP C2 — Tomita-Takesaki is intrinsic per-worldline; supplies no measure over b (machine)
- Per worldline b the state is KMS at κ(b)/2π (free member). Detailed balance verified: the
  bosonic factor 1/(e^{w/T}−1) gives ρ(−w)/ρ(w)=e^{−2πw/κ} (machine; the residual `2e^{..}` was
  only my mis-signed target — the linear ω prefactor flips under ω→−ω, expected).
- Tomita-Takesaki attaches to ONE von Neumann algebra + ONE cyclic-separating vector. Each b gives
  its OWN (algebra, state) ⟹ its OWN modular flow = proper-time flow at rate κ(b)/2π. **There is no
  canonical modular measure GLUEING the different b's.** Modular theory injects b-dependence ONLY
  through the local temperature T_b=κ(b)/2π.
- Edge: κ(b)=H/√(c_χ(c_χ²−b²)) ~ x^{−1/2} (x=c_χ−b) ⟹ T_b ~ x^{−1/2} → ∞ at b→c_χ.
  Machine: /tmp/agentMM_C2.py.

## STEP C3 — The scale/dilatation anomaly cannot deform the spectral exponent (machine)
The residual surviving symmetry is E(3)⋊dilatation, dilatation = proper-time translation, so the
worldline density diagonalizes in the **Mellin variable ν of dilatation** with the scale-invariant
measure (EE 2.5). The natural non-silent candidate is a SCALE anomaly deforming this measure. But:
- The scale/conformal anomaly is a **c-number** (central charge × curvature invariants), a constant
  shift of the effective action. It is **independent of the Mellin spectral parameter ν** and of b.
- Free Mellin kernel |φ̃(ν)|² = πν/sinh(πν) (EE-banked Γ(1−iν) form) — analytic, decaying. The
  anomaly rescales its NORMALIZATION; it injects no ν-power, hence cannot change the edge EXPONENT.
- The free density edge as b→c_χ (κ→∞): ρ ~ κ/2π ~ x^{−1/2}, a smooth classical (Rayleigh–Jeans)
  limit — NO fourth-root, NO oscillation. Machine: /tmp/agentMM_C3.py.

## STEP C4 — The non-local anomaly-induced (Riegert/Paneitz) action gives no fourth-root (machine, HOSTILITY check)
Against a premature "silent": the anomaly is NOT only a c-number — it generates the **non-local
Riegert effective action** with a propagating σ-mode whose propagator is the inverse **Paneitz/GJMS
operator** Δ₄=□(□−2H²) on dS. Tested:
- 1/Δ₄ = (1/2H²)[1/(□−2H²) − 1/□] (machine partial fractions) — **two rational, massive-like KL
  poles**. Polynomial-in-□ ⟹ rational propagator ⟹ POLE (not branch-point) structure in the
  representation/Mellin variable. **A fourth-root x^{1/4} requires a TRANSCENDENTAL dispersion;
  no GJMS/Paneitz operator (polynomial in □) can produce it.**
- The σ-mode is conformally-invariant data on dS ⟹ its b-family pullback is the SAME conformal/DL
  class (EE [2c]), tail = 0, edge power set by κ(b)~x^{−1/2} only. Machine: /tmp/agentMM_C4.py.

## STEP C5 — The modular edge is a SMOOTH POWER, not the Airy fourth-root class (machine, the decisive test)
The one route to x^{−1/4}: u=2π/κ ~ √(c_χ−b) is the Deser–Levin square-root, so a u^{−1/2}
oscillatory density would pull back to x^{−1/4} (the conversion theorem). So Route C is non-silent
**iff** the modular/anomaly structure forces ρ(u) ~ u^{−1/2} cos(γ/√u + φ). It does NOT:
- Free modular density (KMS at T=1/u): ρ(ω)=ω/(1−e^{−ωu}) → 1/u (Rayleigh–Jeans) as u→0 — a
  **simple pole / x^{−1/2} power**, integer-power Laurent (1/(ωu)+1/2+ωu/12+..., machine), **no
  u^{1/2}, no oscillation, no fourth-root**.
- The modular Hamiltonian K=ln Δ is the **boost generator** (Bisognano–Wichmann/Unruh). Its
  spectrum is the **full real line with flat Lebesgue measure** — the thermal/boost class. The PASS
  normal form requires a **negative-argument Airy edge** (−d²+linear ramp → cos(γ x^{−1/4}+φ));
  the boost spectrum has NO confining ramp ⟹ **no Airy edge ⟹ the fingerprint is ABSENT**.
Machine: /tmp/agentMM_C5.py.

## STEP C6 — SCOPED SILENCE (both-ways honesty, machine)
The silence is precise, not a blanket null. The foliation/anomaly **DOES**:
- (D1) **Break dS invariance** — this is the firewall **L7 legality gate**: it moves the problem into
  the invariance-breaking sector where the fourth-root cut is no longer ILLEGAL. NECESSARY-condition
  satisfaction, real and load-bearing — but **not measure-selection**.
- (D2) Fix the residual symmetry to E(3)⋊dilatation ⟹ worldline STATIONARITY ⟹ a positive Mellin/
  Bochner density. Constrains the FORM; leaves the dynamical kernel |φ̃(ν)|²=Ψ FREE.
- (D3) Fix the free member to KMS at κ/2π ⟹ a thermal (pole/power) edge.

The foliation/anomaly **DOES NOT**:
- (N1) Depend on b (C1) ⟹ cannot weight ρ(b).
- (N2) Glue worldlines (C2, T-T intrinsic) ⟹ no measure over the family.
- (N3,N4) Produce a branch point/Airy edge (C3–C5) ⟹ no fourth-root, no oscillation.

**DECISIVE STRUCTURAL REASON.** The fingerprint x^{−1/4}-oscillation must come from the **dynamical
pump kernel Ψ = |φ̃(ν)|²** (EE 2.3), which the anomaly/modular structure leaves FREE. The anomaly
fixes the FRAME (broken dS, stationary worldlines, positive Mellin density); it does not fix the
CONTENT (the b-edge measure / pump spectrum). **Same disjoint-label structure the shared edge map
found:** the anomaly/modular data lives on the SLICING/STATE frame; the fingerprint lives in the
pump dynamics. They do not meet. Machine: /tmp/agentMM_C6.py.

## VERDICT — ROUTE C: the conformal anomaly is SILENT on the family edge measure
The foliation-breaking of dS is **NECESSARY** (it is the legality gate that makes a fourth-root cut
admissible at all — firewall L7) but is **NOT SUFFICIENT and NOT SELECTIVE**: neither the conformal/
scale anomaly (c-number; Riegert/Paneitz = polynomial-in-□, rational/pole edge) nor the modular/
Tomita-Takesaki structure (intrinsic per-worldline; modular K = boost generator, flat spectrum,
thermal edge) **forces** a specific edge measure ρ(b) at b→c_χ. The edge it DOES yield is the
**simple-pole / Rayleigh–Jeans / thermal POWER class (x^{−1/2}), with NO fourth-root and NO
oscillation** — exactly the FREE-EDGE / Watson-thermal class of the shared edge map, reproduced from
the anomaly+modular side independently.

**carries_fourth_root = NO** (computed): the anomaly/modular route delivers the thermal/power edge,
not the x^{−1/4} oscillatory fingerprint.

**The single named calculation that would close or kill it:** classify the **edge spectral-density
normal form of the PUMP's fluctuation operator Ψ on the Deser–Levin family at b→c_χ** (the shared
edge map's primary object). Route C proves this is where the answer lives — the anomaly does not
supply it. PASS = negative-argument Airy edge in Ψ (forced by the pump, NOT by the slicing) → the
fourth-root with γ=γ_req; FAIL = Watson/thermal Ψ → the power edge Route C already exhibits.

**smuggle audit (self-incriminating, mandatory).** Where this derivation could have CHEATED toward
the fourth-root and did NOT:
- I could have declared the Deser–Levin u=√(c_χ−b) map "supplies the fourth-root" by INVERTING the
  conversion theorem (firewall S5/S7: re-present V's σ_req as a derived ρ(b) by riding the √-map).
  AVOIDED: I computed the modular density IN u and found 1/u (pole/power), not u^{−1/2}-oscillatory.
  The √-map is necessary but the OSCILLATORY u^{−1/2} content is absent on the anomaly side.
- I could have hand-selected the conformal (KMS) member's thermality as "the edge structure" and
  dressed κ→∞ as an essential singularity (S9 branch-selection). AVOIDED: the κ~x^{−1/2} divergence
  is a smooth POWER (analytic continuation of a pole), machine-confirmed integer-power Laurent.
- I could have invoked the Riegert action's non-locality as "the transcendental dispersion that makes
  x^{1/4}" (S2: importing the target as the anomaly's output). AVOIDED: Paneitz Δ₄ is polynomial in □
  (machine partial fractions = two rational poles); a polynomial operator's inverse is rational, never
  a branch point. No fourth-root can come from any GJMS/anomaly operator.
- The boost-generator/flat-spectrum identification of K could have been waved as "Airy-like" to force
  the PASS normal form (S3 pre-shaped parametrization). AVOIDED: the boost spectrum is Lebesgue-flat
  with no confining ramp; the −d²+linear-ramp (Airy) operator is structurally absent.
Net: the q=1/4 / fourth-root answer is **not assumed anywhere in Route C** — it is computed ABSENT
from the anomaly/modular sector and explicitly relocated to the free pump kernel Ψ.
