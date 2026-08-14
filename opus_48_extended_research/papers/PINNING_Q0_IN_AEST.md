# Pinning AeST's Free Background Parameter: 𝒬₀ ≈ 3×10⁻³ – 1.5×10⁻² Mpc⁻¹ from Galaxy-Scale Phenomenology

**Carl P. Zimmerman**, Briar Creek Tech
ORCID 0009-0008-3508-7982
2026-08-13 (v4, 2026-08-14: the drain reading settled — the soft low edge becomes operative;
the recombination liability priced at order-of-magnitude grade; and a fixed-point consistency
result — the pin survives its own strongest internal challenge, at the cost of a candidate
transport mechanism.  All three additions adversarially refereed before filing.)

---

## Abstract

The Aether-Scalar-Tensor theory (AeST; Skordis & Złośnik 2021, PRL **127** 161302) reproduces the
Planck CMB power spectrum and the galaxy-scale radial acceleration relation, but leaves the scalar
background rate 𝒬₀ ≡ dφ̄/dt free — its authors state explicitly that the dark-sector density is "not
(classically) predicted." We show that a framework built on AeST with three additional commitments —
the dark-sector charge carrying the full dark-matter abundance (ρ = 𝒬₀ n), the selection β = 1, and
w = −1 exactly — collapses that freedom to a **one-parameter family**, and that galaxy-scale
phenomenology fixes the remaining coordinate. The result is

> **𝒬₀ ≈ 2.4×10⁻³ – 1.5×10⁻² Mpc⁻¹**, equivalently **K″(𝒬₀) ≈ 10² – 10³**,
> *(v4: the low edge is 2.4×10⁻³ under the now-settled steady-state-continuity reading of the
> local charge density — Section 5's "soft by 1.4×" bullet became the operative edge; the v1–v3
> low edge 3.4×10⁻³ was the residence reading)*,

a region strictly interior to AeST's published fits: it lies 45–215× above their exponential fit and
5–20× below their cosh fit, and *excludes* the Higgs-type fit which Skordis and Złośnik themselves
describe as "incompatible with a MOND limit." Expressed in the natural variable
μ ≡ √(K″(𝒬₀)), **both of AeST's MOND-compatible published parameter sets fall inside the pinned band
(μ = 122 and 195, band 33–1295) while the MOND-incompatible one does not (μ = 41231)** — an
independent corroboration, since no CMB information entered the derivation.

We are explicit about what this is not. The pin is an order-of-magnitude *class* statement, not an
equality: the two profiles it equates have different radial shapes and the implied 𝒬₀ drifts by a
factor 2.1–2.7 across 3.7–60 kpc. It does not price the theory's nonlinear sector at recombination,
and cannot: AeST's authors note that a₀ "does not appear in the linear cosmological regime but will
play a role once nonlinear terms from ℱ(𝒴,𝒬) kick in," which is precisely the regime at issue. Every
quantitative claim is reproduced by committed scripts.

---

## 1. What AeST leaves free

AeST is the relativistic MOND-class theory that fits the CMB. Its action is

$$S=\int d^4x\sqrt{-g}\left[\frac{R-2\Lambda_{\rm bare}}{16\pi G}+\mathcal{L}_{\rm aether}[A^\mu,g]+\mathcal{F}(Y,Q)\right]+S_{\rm matter},$$

with the invariants $Q \equiv A^\mu\nabla_\mu\varphi$ and $Y \equiv (g^{\mu\nu}+A^\mu A^\nu)\nabla_\mu\varphi\nabla_\nu\varphi$
built from a unit-timelike aether $A^\mu$ and a scalar $\varphi$. The physical content sits in the
free function ℱ. Skordis and Złośnik exhibit three choices (cosh, Higgs-type, exponential) that fit
Planck, with fitted parameters spanning **four orders of magnitude** in the background rate 𝒬₀:
10⁻⁴, 10⁻¹ and 1 Mpc⁻¹ respectively. Nothing in the theory selects among them.

## 2. The three commitments that collapse the freedom

The framework studied here adds to AeST:

1. **ρ = 𝒬₀ n identically**, with the shift charge carrying the *full* dark-matter abundance. This is
   not an assumption of convenience — it is forced by the shift-symmetric condensate structure, and
   it is the same property that makes w = −1 exact.
2. **β = 1**, the selection fixing the dark sector's scale (the same selection that yields the
   derived evolution law a₀(z)).
3. **w = −1 exactly**, up to 𝒪(ν₀²) with ν₀ ≲ 1.8×10⁻⁴.

Together with the framework's acceleration-scale normalisation
a₀ = κc√(Gρ_Λ) = c²√(Λ/32π) = 9.3619×10⁻¹¹ m/s², these give

$$\mathcal{Q}_0=\frac{\sqrt{\Lambda}\,R_{\rm dm}}{\nu_0\,\mu},\qquad R_{\rm dm}\equiv\Omega_{\rm dm}/\Omega_\Lambda=0.387,\qquad \mu\equiv\sqrt{K''(\mathcal{Q}_0)} .$$

**This is one equation in two unknowns.** The abundance chain therefore does not fix 𝒬₀; it reduces
AeST's freedom to a one-parameter family, parameterised by the dimensionless combination

$$X\equiv\frac{\mathcal{Q}_0c^2}{a_0},\qquad\text{equivalently}\qquad \mathcal{Q}_0\,[{\rm Mpc}^{-1}]=\frac{X}{31112}.$$

## 3. Fixing the remaining coordinate

The framework's kinematic identity $u_\mu=-\nabla_\mu\varphi/s$ — aether-independent, and used
nonlinearly elsewhere in the corpus — slaves the condensate flow speed to the scalar gradient. The
same gradient must simultaneously supply the static MOND force at radial-acceleration-relation radii.
One field, one gradient, two jobs: an equality, which fixes X.

Using AeST's own quasi-static diagonalisation (Φ = Φ̂ + φ with Φ̂ Newtonian), the gate variable is
$y=\left[(g_{\rm tot}-g_N)/a_0\right]^2$, and evaluating it against the framework's own kernel across
3.7–60 kpc with the committed accretion free-fall speed gives

| | X | 𝒬₀ [Mpc⁻¹] | μ = √(K″) |
|---|---|---|---|
| a₀-line kernel | 106 – 323 | 0.0034 – 0.0104 | 33 – 570 |
| MS08 operative kernel | 120 – 453 | 0.0039 – 0.0146 | 40 – 800 |
| defensible envelope | 70 – 1340 | 0.0022 – 0.0431 | 33 – 1295 |

## 4. The corroboration

Nothing above used CMB information. Converting AeST's three *published* fits into the same variable
μ = √(K″(𝒬₀)) (noting that their exponential function carries K″ = 4K₂ rather than 2K₂):

| AeST fit | K₂ | μ = √(K″(𝒬₀)) | inside the pinned band? | MOND-compatible? |
|---|---|---|---|---|
| cosh | 7.5×10³ | **122** | **yes** | yes |
| exponential | 9.5×10³ | **195** | **yes** | yes |
| Higgs-type | 8.5×10⁸ | 41231 | no | **no** — SZ21: "incompatible with a MOND limit" |

Both MOND-compatible published fits land inside the band derived from galaxy-scale phenomenology
alone; the fit their own authors exclude on MOND grounds lands outside it. We regard this as
supporting evidence of the pin's *class*, not as a measurement.

## 5. What this does not establish

Stated as plainly as the result:

- **It is a class, not an equality.** The static-MOND and drain profiles have different radial
  shapes, so exact simultaneity is impossible at any single X; the implied 𝒬₀ drifts by 2.1–2.7×
  across 3.7–60 kpc. This is a real residual, not a rounding.
- **The pin inherits a CANDIDATE grade.** It rests on one adversarially-refereed lane. The
  identification of the corpus's 𝒬₀ with AeST's (units, cosmic time coordinate, background and
  kinetic normalisations) is derivation-grade and was verified on five legs against the published
  source; the *value* is not yet at that grade.
- **The nonlinear sector at recombination is now priced at order-of-magnitude grade (v4), and the
  price is small.** At the pinned 𝒬₀ the theory's 𝒴-sector is genuinely active at z ≈ 1090
  (flow-y ≈ 0.5–280 across the band — the premise is confirmed, not evaded). But the lever arm on
  the dust mode is the vector–scalar mixing share, which scales with 𝒬₀ and is 0.05–0.3% at the
  pinned values (0.5% at the defensible-envelope corner); the kinetic-coefficient deviation is
  bounded by 1, and the 𝒴-branch's direct stress is ~5×10⁻¹⁴ of the dust density. Product: **≤0.2%
  on the core band, ≤0.5% at the envelope** — sub-percent everywhere this note defends. The full
  nonlinear Boltzmann computation remains owed for derivation grade, but it is now a confirmation
  run, not an existential one (`nbody_2026/stage62_cmb_horn_oom_2026.py`).
- **a₀ in this framework is a *local* quantity** — 𝒜(Q) = a₀² = κ²G(−K(𝒬)) depends on the local
  charge density, and the pin's radii (3.7–60 kpc) sit *inside* halos, where that density is orders
  above the cosmic mean. The pin is nonetheless **a₀-free algebraically**: combining X = √y·c/v with
  y = [(g_tot−g_N)/a₀]² and 𝒬₀ = X·a₀/c² gives

  $$\mathcal{Q}_0=\frac{g_{\rm tot}-g_N}{c\,v},$$

  in which a₀ cancels identically — the pin is (MOND excess acceleration)/(c × drain speed), a
  statement in observables. The residual a₀-dependence enters only through the kernel that builds
  g_tot from g_N, is sub-linear (≈ S^0.5 in deep MOND, S^0.8 near y = 1), and is partly opposed by
  v_ff ∝ (GMa₀)^¼ carrying the same factor in the same direction.
- **The low-edge softness is resolved (v4): the steady-state-continuity reading is operative.** For
  the framework's own committed picture — smooth capture, cold radial infall, no halt — mass
  conservation makes ρ = Ṁ/(4πr²v) exact; the residence-time estimate was that same argument with
  an inconsistent (virialised) shape. The 0.0024 Mpc⁻¹ edge is therefore the operative one and is
  carried in the abstract band (`nbody_2026/stage61_drain_reading_fork_2026.py`). The defensible
  envelope of Section 3 is unchanged.
- **A fixed-point consistency result (v4), one each way.** The corpus's candidate "transport
  channel" (an outward shift-charge flux that could have drained the halo's captured charge) turns
  out, at this note's pinned 𝒬₀, to carry a flux that would gate the very accretion flow the pin's
  equality is built on: a strong drain would un-calibrate its own coefficient. **Favourable:** the
  pin survives its strongest internal challenge — the only self-consistent closure is the one that
  leaves the pin's flow intact. **Adverse:** that same argument demotes the transport channel from
  viable-candidate to conditional-dead, closing (at closure grade) a door the framework had open on
  its galaxy-scale dark-matter problem (`nbody_2026/stage63_cell3_transport_1p1d_2026.py`).
- **Consistency note, in the framework's favour:** the same effect is what fixes the framework's own
  ν₀ ceiling — the requirement that the local a₀² shift stay ≲ 1% through the drain is precisely the
  RAR bound on a local a₀, so this is a priced effect rather than an unpriced one.
- **κ = ½ remains measured, not derived** (0.551 ± 0.043 by the distance-free method), and the
  coefficient's origin is unresolved. Nothing here changes that.
- **K₂ is pinned only to ~3 decades**, because the ν₀ window carries a factor 8.3 that propagates
  quadratically. λ_s remains free.

## 6. Why it is worth recording

AeST's parameter freedom in 𝒬₀ is normally regarded as irreducible — its authors say so. The claim
here is narrow and checkable: *if* one commits to the dark-sector charge carrying the full dark-matter
abundance with w = −1 exact, then galaxy-scale phenomenology alone selects a 𝒬₀ region interior to
the published CMB fits, and specifically the region occupied by the MOND-compatible ones. That is a
statement about AeST's parameter space, testable by anyone with the theory and a galaxy sample, and
falsifiable in the obvious way: a CMB fit demanding 𝒬₀ outside 10⁻³–10⁻¹ Mpc⁻¹ would break it.

---

## Reproducibility

All claims are reproduced by committed scripts at
<https://github.com/carlzimmerman/zimmerman-formula>:

- `nbody_2026/stage58_x_to_q0_2026.py` — the conversion identity, the pinned band, the corroboration
  table, and the consequences (9 checks).
- `nbody_2026/stage58_ev_q0pin_lane_2026.py` — the adversarial lane's own trial script (23 checks).
- `nbody_2026/stage56_xpin_verdict_2026.py` — the X-pin and the closure of its named escape route.
- `nbody_2026/stage57_sz21_corrected_refile_2026.py` — the AeST parameter records and the background
  identity SRC = 3f_dust H/𝒬₀.
- `nbody_2026/stage59_local_a0_verdict_2026.py` — the local-a₀ adjudication behind §5's first
  three bullets (7 checks), including the symbolic cancellation.
- `nbody_2026/stage61_drain_reading_fork_2026.py` — the drain-reading settlement behind the v4
  operative low edge (10 checks).
- `nbody_2026/stage62_cmb_horn_oom_2026.py` — the order-of-magnitude pricing of the recombination
  liability (7 checks).
- `nbody_2026/stage63_cell3_transport_1p1d_2026.py` — the fixed-point consistency result (8 checks,
  including the referee-corrected supply-gating mechanism).
- `RETRACTIONS.md` — the standing scope-and-retraction record, including the withdrawal of an earlier
  version of the recombination-side analysis (an error in the framework's *disfavour*, corrected).

**Prior art and attribution.** AeST is Skordis & Złośnik, PRL **127** 161302 (arXiv:2007.00082); the
interpolation kernel used here is Milgrom & Sanders 2008, ApJ **678** 131, Eq. (13) at α = ½. The
framework's contribution is the acceleration-scale normalisation and the three commitments of Section 2,
not the underlying theory.
