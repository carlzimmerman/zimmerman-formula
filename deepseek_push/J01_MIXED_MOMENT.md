# J01 — THE MIXED-MOMENT IDENTITY: E[D v²] in the Thomson sphere
**2026-09-23 · answers the unclaimed `JWST_EQUATION_TARGET` (moment channel)**
Files: `J01_mixed_moment.py` (independent solver) · `J01_mixed_moment.out` (exit 0, 20/20).

**Scope (kept, per the target's own rules):** every statement below is inside
the conservative Thomson-sphere transport model of
`bhstar_scattering_clock_2026_09_21` — stationary sphere, central isotropic
emission, conservative unpolarized Thomson scattering, all photons counted,
no absorption. A model identity is not an observational JWST confirmation and
not a new law of nature; the physics content is that the *mixed moment* is an
independent observable, and the machinery to compute it exactly now exists.

---

## The question (from the target)

The frozen lane proved E[D] = ∫₀¹ r κ(r) dr (Theorem 1, density-free) and, for
uniform isothermal clouds, the lag–width band with σ_sc² = 2 s_e² E[N]. The
target asks for the *exact transport-moment relation* linking the mixed moment
E[v²·D] (equivalently F_pkk(0,0) of the joint Laplace/Fourier transform
F = E[e^{−pD+ikv}]) to the profiles and lower moments — **and to identify and
retain any unclosed angular or boundary term**, with a counterexample if the
lower moments cannot close the relation.

## The theorem (new, verified)

**Conditional on the trajectory, the accumulated Doppler kick v is Gaussian
with variance exactly 2·ang**, where ang = Σ_j T(r_j)(1−u_j·u′_j) is the path
angular exposure: each kick contributes Var(e·(u′−u)) = |u′−u|²·T = 2T(1−μ)
(e independent Maxwellian), and the kicks are conditionally independent. Hence

> **E[D v²] = 2·E[D·ang]** — exact, every scattering order, any bounded
> κ(r) ≥ 0 and T(r) > 0, central or volume source.

Checked on the independent solver at 2e-5 to 2e-3 (MC): uniform (τ₀=1):
E[Dv²] = 3.7316 vs 2E[D·ang] = 3.7237 (Δ 0.2%); q=10: 192.67 vs 192.38
(Δ 0.15%); τ₀=2, q=3, h=2: 234.16 vs 234.04 (Δ 0.05%). The conditional-fourthmoment probe E[v⁴] = 12·E[ang²] also closes (67.05 vs 67.34, and equivalents),
confirming the Gaussian-lemma spine rather than a two-moment accident.

### Where it sits in the hierarchy

The target's candidate BVP is confirmed (first-step conditioning): the tilted
collision factor exp[−k²T(r)(1−u·u′)] is exactly the averaged Maxwell kick
phase, and the p,k expansion of

    u·∇F + κ(r)[∫P(u,u′)e^{−k²T(1−u·u′)}F(x,u′)dΩ′ − F] − pF = 0,   F = e^{px·u} on |x|=1

gives the moment hierarchy (signs verified numerically, not asserted):

| order | equation | value at center |
|---|---|---|
| 0 | F⁰⁰ = 1 | — |
| p | L F¹⁰ = 1, F¹⁰\|_b = x·u | −E[D] = −∫₀¹ rκ dr  ✓ benchmark |
| k² | **L F⁰² = 2κ(r)T(r)**, F⁰²\|_b = 0 | F⁰² = −2·E[ang] = −E[v²] ✓ exposure identity |
| **pk²** | **L F¹² = F⁰² + 2κT∫P(u,u′)(1−u·u′)F¹⁰**, F¹²\|_b = 0 | **E[D v²] = −∂_p∂_k²F** |

L = u·∇ + κ(P − 1). The factor 2 is the tilt's quadratic term (∂²_k
e^{−k²T(1−u·u′)}|0 = −2T(1−u·u′)) — it appears in **both** the F⁰² source
(2κT) and the mix source (2κT∫P JF¹⁰), and it is what makes
F⁰²(0) = −2E[ang] consistent with Lψ = g ⟹ ψ(0) = −E[∫g dt] (verified:
E[v²] = 2E[ang] numerically). The F¹² source is a *T-weighted
Thomson-cone average of the delay field F¹⁰* — the angular term the target
asked to retain. The numerically verified statement is the identity
E[Dv²] = 2E[D·ang]; the hierarchy is its exact BVP image (order-by-order
re-derivation of the tilted equation, signs re-checked).

## The unclosed term, quantified (the target's counterexample)

The naive two-moment closure E[D v²] = 2·E[D]·E[ang] is **false**: the
correlation ratio

    R = E[D v²] / (2 E[D] E[ang])

is measured (n = 5×10⁵, ±SE) at

| profile (τ₀=1, h=0) | R | ±SE |
|---|---|---|
| uniform q=0 | 2.6446 | 0.018 |
| q=3 | 2.0235 | 0.012 |
| q=10 | 1.6971 | 0.009 |

R is a pure function of the density shape (5σ+ separations), so **no
assignment of {E[D], E[v²], E[N]} closes the mixed moment** — the angular
correlation Cov(D, ang) is load-bearing. This is the counterexample the target
demanded, and it isolates the required observable: the *joint* statistics of
D and the Thomson-cone-weighted delay field, i.e. F¹²'s source term, not any
of the marginal moments. (Matching the target's sentence: a matched pair
fixing two moments is not a counterexample to determination by the full
spectrum — and equally not a closure of the mixed moment.)

## Independent-solver discipline

`J01_mixed_moment.py` is a from-scratch event-driven engine: exact
optical-depth sampling via bisection on the exact rate integral (no
null-collision acceptance, no shared arithmetic with
`bhstar_scattering_clock_2026_09_21/transport.py`), reconstruction of the
Thomson azimuth from scratch, own seeds and geometry. Calibration against the
frozen `transport.py` at shared (τ₀=1, q=0, h=0, central): E[D] = 0.5023 vs
0.4985 (0.8%), E[v²] = 2.817 vs 2.833 (0.6%) — both engines agree on the same
physics; every benchmark of the frozen lane is reproduced (E[D] = ∫rκ dr to
0.24%; E[v²] = 2E[N] isothermal to 0.02%; exposure = angular identity).

## Honest edges (per the promotion rules)

- New content: the exact mixed-moment identity E[D v²] = 2E[D·ang], its
  position in the F-hierarchy, and the measured non-closure of the marginal
  moments (R ≠ 1). The BVP and the tilted factor are the target's own
  candidate — verified here, not invented.
- Not claimed: no observational JWST confirmation (no LRD data touched), no
  new law of nature, no global novelty certificate (the Bal/Jollivet/Patat
  overlap for adjacent scattering-order statistics was never resolved in the
  lane and is not addressed here; the mixed moment on a sphere is a transport
  calculation in a standard model, and that boundary is kept explicit).
- The identity is exact within the model; the numbers are MC estimates with
  reported standard errors, not proofs of values (the identity itself is
  proven by the conditional-Gaussian lemma + the pathwise definition of D
  and ang — no asymptotic order is involved).