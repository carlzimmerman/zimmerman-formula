# A Two-Degree-of-Freedom York/CMC MOND Theory and a No-Go for its Causal Relativistic Lensing Completion

**Status: FROZEN DEFENSIBLE RESULT.** This is a *construction + no-go* result, not a claim to
have solved relativistic MOND. Every load-bearing statement is backed by a committed, runnable
script in `qwen_claude_field_theory/theory_2026/york/`. Honest ceilings are stated up front:
**κ and Z are postulated/fitted, not derived; the no-go is conditional on the stated
operator/locality/single-metric assumptions.**

---

## Abstract

We construct and analyze a York/CMC formulation of a MOND-like gravitational theory with two
propagating tensor degrees of freedom and no propagating scalar mode. The gravitational
coefficients are selected within the chosen operator basis to (ξ, η) = (1, 0) by c_T = 1 and the
metric-sector G_eff = G; the nonlinear constraint algebra contains a second-class (P_Φ, C_Φ) pair
that removes the would-be scalar, verified directly (not as a singular limit) including a
cubic/quartic strong-coupling check. The cosmological construction yields **a₀(z) = a₀,₀ H(z)/H₀**
(evolution law derived and Z-independent; absolute normalization postulated). We then prove that
this theory cannot be promoted to a *causal, single-metric, local* relativistic MOND theory with
correct gravitational lensing while retaining the two-DOF structure: (i) a local disformal physical
metric that preserves 2+0 cannot supply the lensing phantom, and any lensing-sized disformal splits
the photon/graviton cone (GW170817); (ii) the passive/AQUAL stress under-supplies the lensing source
(the ν² gap) and a local acceleration functional is mass-blind; (iii) an elliptic phantom carrier
reproduces the static MOND lensing source but makes the physical potential instantaneous, an
acausal channel because matter couples to it directly. The obstruction is the same structural
trade-off that led relativistic MOND (TeVeS, AeST, DEW) to introduce additional dynamical fields or
abandon the horizon-tied a₀.

---

## 1. The frozen theory

Khronon normal and spatial projector:

    u_μ = −∇_μ T / √(−∇_α T ∇^α T),   h_μν = g_μν + u_μ u_ν

Gravitational sector (York/CMC-reduced GR; **CMC as a global gauge-fixing**, not a local
Λ_CMC(K−q) multiplier — the two are inequivalent, see §6):

    S_Y = (M_Pl²/2) ∫ d⁴x N√h [ K_ij K^ij − K² + ³R ],   K = K_CMC(t)

MOND scalar (constrained/elliptic, quasistatic representation):

    ∇²Ψ = 4πGρ,   ∇²Φ = ∇·[ ν(|∇Ψ|/a₀) ∇Ψ ],   ν(y) = √(1 + 1/y)   ⇒   g_MOND² = g_N² + a₀ g_N

Cosmological scale (from the CMC clock, K = q, q_FLRW = 3H):

    a₀(z) = a₀,₀ H(z)/H₀        [DERIVED evolution law]
    a₀ = κ c √(Gρ_Λ)            [absolute normalization: κ, Z POSTULATED/FITTED]

---

## 2. Positive result — the two-DOF theorem

**Theorem (2-DOF).** In the York/CMC global-gauge-fixing formulation at (ξ, η) = (1, 0), the theory
has exactly two propagating tensor DOF; the MOND scalar Φ is removed from the local propagating
phase space by a second-class constraint pair.

Established, script-backed:
- `dof_deformed_cmc_2026.py` — Φ second-class; H_⊥ Dirac–DeWitt algebra closes (MOND density
  ultralocal in h); count = 2.
- `york_step2_closure_2026.py` — smeared {H_⊥[N],H_⊥[M]} = H_i[…] (MOND term contributes zero);
  Dirac chain terminates; Φ-operator convex/invertible.
- `frozen_dirac_hamiltonian_2026.py`, `frozen_dirac_sectors_2026.py` — for the general khronometric
  action the count is 2+1 (a khronon propagates); **c_T=1 forces ξ=1 and metric G_eff=G forces η=0**,
  which is the unique 2+0 point (derived, not fitted). The local-Λ_CMC form is 3-DOF; only the York
  global gauge-fixing is 2-DOF.
- `eta0_direct_dirac_2026.py` (34/34) + `eta0_cubic_quartic_2026.py` (18/18) — the η=0 theory
  certified DIRECTLY: (P_Φ,C_Φ) det = B² = (N√h·2P(Y))², P(Y)=√y(y+2)/(1+y)^{3/2}>0; chain
  terminates, no tertiary; cubic/quartic vertices finite ∀ Y₀>0 (no strong coupling). Referee-
  reproduced. The zero-acceleration set Y=0 is a documented measure-zero degenerate-elliptic
  boundary (PDE regularity, **not** a rank change).

The auxiliary QUMOND carrier (Ψ, χ, λ) is likewise 0 local DOF: Hessian det H = k⁶, full Dirac
det Δ = k¹²; det Δ_aux = (det V_AB)² survives arbitrary regular spatial couplings to h_ij.

## 3. Cosmological scale

`cosmology_flrw_2026.py` — on flat FLRW, D_iΦ=0 ⇒ U(0)=0 ⇒ the MOND stress vanishes identically
(no Λ_eff, no G rescale); K = −3H ⇒ a₀ = 3cH/Z ⇒ **a₀(z)/a₀,₀ = H(z)/H₀, Z-independent.**

---

## 4. Negative result — the relativistic-lensing no-go (three independent obstructions)

**(a) Local disformal completion FAILS.** With g̃ = C(Φ,σ)g + D(Φ,σ)u_μu_ν, σ=|D_iΦ|²
(`gate2_dof_preservation_2026.py`): a nonzero *foliation-spatial* D preserves 2+0 (covariant-X
injects Φ̇² → 2+1). But (`gate2_lensing_2026.py`, `gate2_cone_gw170817_2026.py`,
`gate2_hostile_referee_2026.py`): the unique gap-closing D = −4φ_ph, φ_ph = Φ − ∇⁻²∇·[μ∇Φ], is
**non-local** (outside the 2+0 class), and c_γ² = (C−D)/C with luminal gravitons ⇒ c_γ²−c_GW² = −D/C,
so a lensing-sized D/C = O(ν−1) violates GW170817 (|D/C| ≲ 2×10⁻¹⁵) by ~15 orders. {2+0}∩{lensing}∩
{luminal} = ∅ (over-determined; referee-sustained).

**(b) Passive/AQUAL stress is mass-blind.** The passive single-metric stress gives ρ_eff ~ ρ/ν
where MOND lensing needs νρ = ρ + (ν−1)ρ (the ν² gap). A universal local F(K) cannot know which
source mass produced the local acceleration (F′_req ∝ √M), giving an ≈41× galaxy/cluster mismatch.

**(c) Elliptic phantom carrier ⇒ instantaneous physical channel.** The QUMOND carrier
∇²Φ = ∇·[ν∇Ψ] supplies exactly ρ_ph = (1/4πG)∇·[(ν−1)∇Ψ] at 2+0, single-metric (so c_γ=c_GW=1 and
Φ_phys=Ψ_phys ⇒ g_lens=g_dyn=νg_N). But Φ is fixed by an *elliptic slice equation* from ρ, and
**matter couples directly to Φ**, so a change in ρ shifts distant accelerations on the same slice
with no null signal — a physical (super-luminal) channel. Unlike GR (elliptic constraints fix
initial data; physical DOF hyperbolic), here Φ *is* the force law. The CMC preferred foliation does
not launder this (cf. Hořava instantaneous-mode Cauchy-problem issues). Hyperbolizing the carrier
makes it propagate: 2+0 → 2+1.

**The trilemma.** {MOND lensing} + {2 local gravitational DOF} + {causal single-metric} — pick two.

---

## 5. The two formal theorems

> **Two-DOF theorem.** In the specified York/CMC global-gauge-fixing framework at (ξ,η)=(1,0),
> the gravitational sector has two propagating tensor degrees of freedom, and the MOND scalar
> sector is removed from the local propagating phase space by its nonlinear constraint structure.

> **No-go theorem.** Within this two-local-gravitational-DOF framework, a MOND lensing completion
> cannot simultaneously be local, single-metric, and causal while keeping the MOND sector
> non-propagating. Local disformal completions fail the lensing/cone requirements; elliptic phantom
> carriers reproduce the static MOND lensing source but introduce an instantaneous physical channel;
> restoring causality requires an additional propagating field (2+0 → 2+1).

Assumptions (stated for the no-go): (A) two local gravitational DOF; (B) single physical metric for
matter and light; (C) the MOND sector is non-propagating (elliptic/constrained); (D) the completion
operators are local and foliation-spatial. Relaxing any one has a known escape (nonlocal metric MOND
à la DEW — but a₀ becomes a free coupling; or a propagating vector à la AeST — but 2+0 is lost).

---

## 6. Honest status and scope

| Requirement | Result |
|---|---|
| 2 tensor DOF | ✓ (certified, referee-sustained) |
| a₀(z) ∝ H(z) | ✓ within the stated construction (evolution law derived, Z-independent) |
| MOND weak-field dynamics | ✓ (g² = g_N² + a₀ g_N) |
| static MOND phantom source | ✓ (elliptic carrier, ρ_ph = (ν−1)ρ) |
| local causal relativistic lensing | ✗ (three-obstruction no-go) |
| complete viable relativistic theory | ✗ |

Ceilings (do not overstate): **κ = ½ and Z ≈ 21 are postulated/fitted**, not first-principles —
only the a₀(z) *proportionality* is predicted. The no-go is conditional on assumptions A–D. PPN/
Cassini (the inherited μ-function EFE-Q₂ ~ few-σ liability), cosmological perturbations, full
hyperbolicity, and an independent replication of the committed Dirac scripts remain open/owed.

**One-line result:** a nonlinear 2-DOF York/CMC MOND EFT that predicts a₀(z) ∝ H(z), together with
a no-go theorem explaining — from a cleaner starting point than TeVeS/AeST/DEW — why its causal,
single-metric, 2-DOF relativistic lensing completion does not exist.
