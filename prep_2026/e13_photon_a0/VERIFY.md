# VERIFY — E13 photon-a0 (exact elliptic deflection fit to Brouwer+2021 lensing RAR)

Adversarial re-verification of `e13_fit.py`. Independent re-derivation + re-eval, not a re-run.
Judged on the framework's own terms (horizon-derived a0, its own disformal E13 deflection).

## 0. Re-run
`python3 e13_fit.py` → **exit 0**. All printed numbers reproduce
(a0_E13 = 2.514e-10 [2.396,2.636], chi2 38.8/14; a0_alg = 1.974e-10, 38.9/14; ratio 1.273; dchi2 −0.09).

## 1. E13 limits — re-checked with an INDEPENDENT elliptic eval (raw mpmath quadrature, not scipy)
- Einstein inner (u→0): alpha/(4GM/c^2 b) = 1.0000000 ✓
- Mortlock-Turner outer (u→∞): alpha/(2π√(GM a0)/c^2) = 1.0000000 ✓ (credited Mortlock-Turner 2001)
- Hand re-derivation confirms both: √(1+u²)E(m)→1 (u→0), and →u·(π/2) with GM/r_M=√(GM a0) (u→∞).
- Convention note (honest): the E13 argument 1/(1+u²) is read as the **parameter m** (scipy `ellipe(m)`).
  The two endpoint limits are convention-BLIND (m and m² both →1 at the knee, →0 in the deep limit), so
  they do not by themselves fix m-vs-k. What fixes it is that the closed-form transfer uses E(m) AND K(m)
  **consistently in m**, and the deep coefficient then comes out **exactly √(π/4)=0.8862** and the fit ratio
  **exactly 4/π=1.273** — an internal-consistency anchor that holds regardless. VERDICT: limits CONFIRMED.

## 2. alpha → ESD map — re-derived from scratch, matches the script
For an axisymmetric lens α(b)=4G·M2D(<b)/(c²b) ⇒ Σ̄(<b)=c²α/(4πGb), Σ(b)=(c²/8πGb)d(bα)/db, so
**g_obs = 4G·ESD = (c²/2π)(α/b − α′)**. Same operator on a baryonic point mass (α_bar=4GM/c²b) gives
**g_bar = 4GM/(πb²)** — the geometric 4/π is identical in g_obs and g_bar and cancels in the RAR
(RAR→g_obs=g_bar, exactly P2's fit assumption). Substituting E13 (with the exact identity
S′(u)=uK(m)/√(1+u²), which I re-derived via dE/dm=(E−K)/2m):
**T(u)=g_obs/g_bar=[(1+u²)E(m)−(u²/2)K(m)]/√(1+u²), m=1/(1+u²), u²=4a0/(π g_bar) (mass-independent).**
Independent numerical build of 4G·ESD by symmetric-differencing α(b) — at three masses (1e9,1e11,1e13 Msun)
— matches the closed form to **max frac diff 1e-11** and is mass-independent. Deep limit T→(π/4)u ⇒
g_obs→√((π/4)a0 g_bar); the −α′ convergence term is essential (Σ̄-only shortcut would give √π=1.77, wrong).
VERDICT: map CONFIRMED, exact, no approximation.

## 3. INFORMATION QUESTION (core) — independent pin, or repackages P2?  → **REPACKAGES P2**
- **Loader is P2's, faithfully.** E13's algebraic branch = 1.974e-10 @ chi2 38.9/14; running
  `p2_lensing_a0_band.py` gives **1.975e-10 @ 38.9/14** — identical. Same 15 points, same full covariance GLS.
- **The exact shape adds NO leverage in the mass-collapsed RAR plane.** After the deterministic 4/π rescale,
  E13 and the algebraic ν transfers differ by **< 0.18% in g_obs across the ENTIRE Brouwer range** — far below
  the 5–15% data errors. Consequence: **Δχ²(E13 − alg) = −0.09**, i.e. the elliptic curvature is unresolved.
- **Why: the data never reaches the Einstein knee.** Headline g_bar ∈ [1.4e-15, 3.9e-12]; at the least-deep
  point u = √(4a0/π g_bar) ≈ **9** (all other points deeper). The knee where elliptic-vs-algebraic curvature
  would separate is at u≲1 — outside the data. So the two shapes differ **only in normalization**, which is
  100% degenerate with a0. a0_E13 = (4/π)·a0_alg is a **deterministic one-number map**, not new information.
- **σ(a0) budget:** stat σ ≈ 1.2e-11 (**4.8%**); systematic band [9.21e-11, 4.18e-10] = **factor 4.5**,
  systematic/stat ≈ **14×**. The M*±0.2 dex baryon-scale term alone swings 1.58e-10↔3.99e-10 (factor 2.5);
  B21's own hot-CGM file → 9.70e-11. **Baryon-budget-limited, exactly like P2 — the shape fit does NOT escape it.**

## 4. Baryon-budget honesty
P2's [7.23,32.8]e-11 baryon-dominated band is **inherited, not escaped** — shifted up by the fixed 4/π to
[9.21e-11, 4.18e-10]. The dominant systematic is the lens baryon budget (stars+cold gas vs hot CGM),
which B21 themselves flag; shear+photo-z (the truly photon-specific terms) move a0 only ~10%.

## 5. Manufactured-concordance and manufactured-null hunt (both directions)
- **Manufactured WIN?** None found. The "concordance" is real but WEAK: canonical 9.355e-11 sits near the band
  **FLOOR** (fiducial best fit is 2.69× canonical, WORSE than P2's algebraic 2.11×; canonical survives only at the
  hot-CGM/maximal-baryon end). The script does not claim "lensing pins 9.36e-11" — correctly, band factor 4.5.
- **Manufactured NULL / hidden deficit?** None. The 2.69× "high" reading is NOT a deficit: it is the 4/π
  convention-coupling between the exact point-mass cylindrical deflection and Brouwer's 4G·ESD definition —
  deterministic, and the band still straddles both Planck footings and the kinematic gas-dominated line
  (0.92–1.18e-10). Reading raw 2.51e-10 as "a0 is 2.7× high" would be the manufactured null; correctly avoided.
- Both footings tested (canonical 9.355e-11, alt 1.131e-10); both INSIDE. No "proves" language anywhere.

## VERDICT
**REPACKAGES P2 (genuine photon-side concordance datum, NOT an independent narrowing pin; the exact E13
deflection shape adds NO shape information in the mass-collapsed RAR plane).** a0_photon(E13) = 2.514e-10,
= (4/π)·a0_photon(algebraic), a deterministic recalibration of the same Brouwer fit — systematics disjoint
from the kinematic RAR (shear/photo-z/lens baryon budget vs M/L/distance/inclination), so it is a real
independent-systematics concordance check, and it PASSES (band contains both footings + the kinematic line).
But it does not tighten a0: baryon-budget-limited (σ_sys/σ_stat ≈ 14), and the data (u≳9 throughout) cannot
resolve the elliptic curvature from the algebraic ν (Δχ² = −0.09). The exact deflection's genuinely new,
testable content lives at **fixed lens mass** — the saturated-deflection shelf (B21 Fig-9 mass bins / Euclid)
— NOT in the RAR plane where r_M and the shape degenerate into the single 4/π normalization.
No open door closed; no "theory closed"; no win and no deficit manufactured.
