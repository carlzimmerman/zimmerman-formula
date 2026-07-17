# E13 PHOTON a0 — the exact elliptic deflection fit to Brouwer+2021 weak-lensing RAR

**Script:** `e13_fit.py` (exit 0). **Output:** `e13_fit.json`. Data: Brouwer et al. 2021
(A&A 650, A113) KiDS-1000 isolated-lens RAR, authors' own machine-readable release (frozen
repo, read-only). Loaders reused verbatim from `concordance_ledger/p2_lensing_a0_band.py`.

## What was built
The EXACT E13 point-mass deflection `alpha(b)=(4GM/c^2 b)·sqrt(1+u^2)·E(1/(1+u^2))`
(u=b/r_M, r_M=sqrt(GM/a0)) mapped — with NO approximation — to the observable Brouwer
reports (g_obs = 4G·ESD), then fit for a0 both footings against the P2 algebraic ν, on the
same data + full covariance.

## The derivation (deflection → the Brouwer observable, exact)
Stacked lensing measures ESD(b)=Σ̄(<b)−Σ(b); B21 (README Eq. 7) report g_obs=4G·ESD.
For an axisymmetric lens the physical deflection is the enclosed-2D-mass relation
`alpha(b)=4G·M2D(<b)/(c^2 b)`, giving `Σ̄(<b)=c²α/(4πGb)`, `Σ(b)=(c²/8πGb)d(bα)/db`, so

> **g_obs = 4G·ESD = (c²/2π)(α/b − α′)**.

The same convention on a baryonic point mass (α_bar=4GM/c²b) gives g_bar=4GM/(πb²); the
geometric (4/π) is identical in g_obs and g_bar and **cancels in the RAR** (their RAR
asymptotes to g_obs=g_bar, exactly the assumption P2's fit form encodes). Substituting E13's
deflection, the lens mass **drops out of the RAR plane** and the exact lensing transfer is a
closed form:

> **g_obs = g_bar · T(u),  T(u) = [(1+u²)E(m) − (u²/2)K(m)] / √(1+u²),  m=1/(1+u²),
> with u² = 4a₀/(π g_bar)** (mass-independent).

E and K are the complete elliptic integrals (2nd, 1st kind). Derivation of T uses the exact
identity S′(u)=uK(m)/√(1+u²) where S(u)=√(1+u²)E(m). a₀ enters purely through
u²=4a₀/(πg_bar); r_M=sqrt(GM/a₀) is the Einstein→MOND transition impact parameter for a
given lens mass, but collapses out of the RAR plane.

**Limits (all verified numerically in-script):**
- Einstein u→0: α→4GM/c²b, T→1, g_obs→g_bar (machine precision).
- Mortlock–Turner u→∞: α→α_∞=2π√(GMa₀)/c² (machine precision); T→(π/4)u, so the deep
  lensing asymptote is **g_obs → √((π/4)·a₀·g_bar)**, i.e. coeff **√(π/4)=0.886** relative to
  standard deep-MOND √(a₀g_bar). (The naïve Σ̄-only shortcut would give √π=1.77; the −α′
  convergence term is exactly why "do NOT approximate" matters.)
- Closed-form T(u) vs a direct numerical 4G·ESD built by differentiating α(b): max frac diff
  **7×10⁻¹⁰** — the closed form is the exact ESD, independently confirmed.

## The fit (both footings, full covariance, GLS)
| model | a₀ (m/s²) | stat [Δχ²=1] | χ²/dof |
|---|---|---|---|
| **E13 exact elliptic** | **2.514e-10** | [2.40e-10, 2.64e-10] | 38.8/14 |
| P2 algebraic ν | 1.974e-10 | [1.88e-10, 2.07e-10] | 38.9/14 |

- **a₀(E13)/a₀(alg) = 1.273 = exactly 4/π** — the fit reproduces the analytic deep-coefficient
  prediction to 3 digits (prove-by-moving-the-number).
- **Δχ²(E13 − alg) = −0.09.** The data **cannot distinguish** the exact elliptic shape from the
  algebraic ν: over Brouwer's g_bar range both are dominated by the deep power law, where they
  differ only in *normalization*, which is fully degenerate with a₀. The elliptic *curvature* is
  not resolved.

**E13 systematic band** (this probe's own budget — shear ±5%, photo-z, and the dominant
baryon-budget term; all disjoint from the kinematic M/L–distance–inclination systematics):
**[9.21e-11, 4.18e-10] m/s²**, factor ~4.5 wide, set by the baryon budget exactly as in P2.
Hot-CGM (maximal baryon) budget → 9.70e-11; fiducial (stars+cold gas) → 2.51e-10.

## Concordance
- Both Planck footings **INSIDE** the E13 photon band: canonical 9.355e-11, alt 1.131e-10.
- Kinematic gas-dominated a₀-line **[0.92, 1.18]e-10 overlaps** the E13 band → the photon-a₀
  concords with the kinematic a₀ (a real, systematics-disjoint datum).
- Fiducial-budget best fit 2.51e-10 = 2.69× canonical (the 4/π shift makes the fiducial-budget
  tension modestly *worse* than P2's 2.11×; canonical survives only toward the hot-CGM / maximal
  baryon end of the budget — an honest cost of using the exact shape).

## VERDICT — repackages, does not newly pin
The exact E13 deflection shape departs from the algebraic ν by **one deterministic factor,
√(π/4) in the deep asymptote → a fixed 4/π=1.273× recalibration of the recovered a₀**. That is
its entire effect on the collapsed lensing RAR. Because the elliptic curvature is unresolved
(Δχ²=−0.09) and the band is dominated by the same baryon-budget uncertainty as P2, the exact
shape **adds no new leverage** and **does not narrow** the photon-a₀. The E13-lensing photon-a₀
therefore **REPACKAGES the P2 band with a deterministic 4/π shift** — it is a genuine
photon-side concordance datum (band contains both footings and the kinematic line), but **NOT a
new independent pin** of 9.36e-11. Honest both ways: no "lensing pins a₀" (band factor ~4.5
wide), no deficit ("lensing excludes canonical" is false — the budget bracket straddles it).

The exact deflection's genuinely new, testable content lives **at fixed lens mass** — the
saturated-deflection *shelf* (α→α_∞, b-independent) in the Fig-9 mass bins / future Euclid–Rubin
stacks — **not** in the mass-collapsed RAR plane, where both r_M and the elliptic shape
degenerate away into the single 4/π normalization.

## Caveats
- Point-mass idealization: valid where lensing probes b ≫ baryonic scale (the deep/outer
  points that dominate the fit); innermost high-g_bar points carry extended-baryon corrections
  but there T→1 regardless, so they don't drive a₀.
- The 4/π is a convention-coupling between the exact point-mass cylindrical deflection and
  Brouwer's 4G·ESD acceleration definition; it is deterministic and exact, but it means the
  *number* a₀(E13) is only comparable to kinematic a₀ through this fixed map — do not read the
  raw 2.51e-10 as "a₀ is 2.7× high," read the band.
- Mistele–McGaugh 2024 (arXiv:2310.15248, JCAP 04(2024)020): cited qualitatively — their
  lensing RAR "smoothly continues" the kinematic RAR ~2.5 dex deeper with SPARC-consistent
  masses; no machine-readable point table found on arXiv/Zenodo (consistent with the frozen
  P2 lane's finding as of 2026-07-16).
- Single stat realization; grid a₀∈[2e-11,8e-10]. No "proves" language: the null (no new pin)
  was verified as hard as the concordance.
