# EQUATION BOOK — LANE M2 (seams S2 thermal/Unruh · S4 kernel/spectral · S6 lensing · S7 cluster throttle)

**Date:** 2026-07-16. **Framework:** de Sitter–Unruh MODIFIED INERTIA (Carl Zimmerman) — judged on its
OWN premises throughout: ν(y)=√(1+1/y), g_obs=√(g_bar²+g_bar a₀), μ(x)=K(x²)=(√(1+4x²)−1)/(2x),
kernel K(z)=(√(1+4z)−1)/(2√z) Herglotz with the unique measure ρ_A=(1−√(1−4|t|))/(2π√|t|) on (−¼,0),
ρ_B=1/(2π√|t|) below, sum rule ∫dμ/|t|=1, τ_mem=2c/a₀, κ_eff=√(H²+(a/c)²), disformal lensing B fixed by
the same K (UNIFICATION.md U2), y_c=Z/2 throttle (Branch B). **Both footings everywhere:**
canonical a₀ = cH_Λ/Z = 9.362×10⁻¹¹ m/s² (ρ_DE) / alt a₀ = 1.130×10⁻¹⁰ (ρ_total/cH₀); Z=√(32π/3)
footing-free.

**Scripts (all exit 0, no hard-coded booleans; outputs `.out` alongside):**
`s2_thermal_identities.py` (12 checks), `s4_kernel_spectral.py` (44), `s6_lensing_closed_form.py` (14),
`s7_throttle_closed_form.py` (22), `m2_massline_sparc_fire.py` (SPARC quick fire, read-only frozen repo).

**Archetype being extended:** the a₀-line — squaring the law gives g_obs² − g_bar² = a₀·g_bar EXACTLY
(a zero-fit linear identity: the RAR as a slope measurement).

---

## THE MINED EQUATIONS (ranked; rubric N/T/D/U = novelty, testability, derivedness, utility, each /5)

### 1. E-S6-3 — THE DEFLECTION CLOSED FORM (complete elliptic E) — **headline** [N5 T4 D5 U5 = 19]

For a point (or compact spherical) mass M under the framework's own disformal lensing
(deflecting field = the RAR field g_obs, UNIFICATION.md U2), the weak-field deflection is,
**at every impact parameter b, in one line**:

$$\boxed{\ \alpha(b)\;=\;\frac{4GM}{c^2 b}\,\sqrt{1+u^2}\;E\!\left(\frac{1}{1+u^2}\right),
\qquad u=\frac{b}{r_M},\quad r_M=\sqrt{GM/a_0}\ }$$

E = complete elliptic integral of the second kind (parameter convention m).
- **Limits verified exactly:** b≪r_M → 4GM/c²b (Einstein, E(1)=1); b≫r_M → α_∞ = 2π√(GMa₀)/c²
  (the known deep-MOND flat deflection — that asymptote is Mortlock & Turner 2001 / standard MOND
  literature, credited, *not* claimed).
- **Approach law (new, an a₀-estimator from lensing shape):** α(b) = α_∞·[1 + r_M²/(4b²) + O(u⁻⁴)].
- **Numbers:** M=10¹¹ M⊙: r_M = 12.2/11.1 kpc, α_∞ = 0.508″/0.558″ (canonical/alt).
- **Why closed form exists at all:** this ν makes g_obs = √(GMa₀)·√(r_M²+r²)/r² algebraic — the
  framework's own interpolation is what turns the lensing integral elliptic. (No uniqueness claim.)
- **Flags:** EXACT within the framework's weak-field, thin-lens, **spherical** (closure-pinned),
  isolated (no-EFE) construction; off-sphere it inherits gap A like everything else (UNIFICATION §5b).
- **Novelty check:** WebSearch — MOND point-mass lensing exists as *piecewise sharp-μ* arctan forms
  (Mortlock & Turner 2001, astro-ph/0106100) and the deep-MOND constant; **no elliptic-integral
  closed form for a smooth interpolation found.**
- **Testability:** galaxy–galaxy stacked lensing (KiDS/DES/Euclid) measures exactly this α(b)/ΔΣ(b)
  shape around isolated galaxies; the +r_M²/4b² approach term is the falsifiable shape signature.

### 2. E-S6-1 — THE MASS-LINE / MASS HYPERBOLA (the lensing Σ-line analog of the a₀-line) [N4 T5 D5 U5 = 19]

Point mass: $\;M_{\rm eff}(r) = g_{\rm obs}r^2/G = M\sqrt{1+(r/r_M)^2}\;$ — the effective (dynamical =
lensing) mass grows on an exact hyperbola. **General spherical system, exact at every r:**

$$\boxed{\ G\left[M_{\rm eff}(r)^2 - M_b(r)^2\right] \;=\; a_0\, M_b(r)\, r^2\ }$$

- The a₀-line transported to **mass coordinates**: plot G(M_eff²−M_b²)/M_b against r² → a straight
  line through the origin with slope a₀, zero fit parameters. M_eff can come from *deprojected
  lensing* — and because B is fixed by the same kernel, the framework REQUIRES the lensing mass-line
  slope to equal the kinematic a₀-line slope exactly (a falsifiable equal-slope consistency test that
  MG theories with independent lensing sectors need not pass).
- **Quick data fire (SPARC, read-only, `m2_massline_sparc_fire.py`, exit 0):** the estimator runs
  end-to-end on 175 galaxies / 3389 points; robust median a₀̂ = 1.40/1.05/0.81/0.63 ×10⁻¹⁰ at
  Υ=0.5/0.6/0.7/0.8 — **brackets BOTH footings inside the physical Υ range; NON-diagnostic between
  footings (as banked; no win, no deficit).**
- **Methodological finding (new, load-bearing for the whole a₀-line workflow):** the naive
  WLS-through-origin slope of g_obs²−g_bar² vs g_bar is **biased low ~3×** (2.7e-11 at Υ=0.7 vs
  median 8.1e-11) because the difference of squares inherits sign-definite M/L-correlated
  g_bar-side errors at high y. **The a₀-line must be fit with a robust/median estimator, a low-y
  band, or full errors-in-variables — never naive WLS.**

### 3. E-S4-1 — THE MEMORY FUNCTION IN CLOSED FORM (time-domain kernel of the published action) [N5 T2 D5 U4 = 16]

The unique Herglotz measure gives the causal-retarded time-domain representation
K̂f(τ) = f(τ) − ∫₀^∞ Γ(s) f(τ−s) ds with, **exactly** (b = s/τ_mem, τ_mem = 2c/a₀):

$$\boxed{\ \Gamma(s) \;=\; \frac{1}{\tau_{\rm mem}}\int_{s/\tau_{\rm mem}}^{\infty}\frac{J_1(x)}{x}\,dx
\;=\; \frac{1}{\tau_{\rm mem}}\Big[\,1 + J_1(b) - bJ_0(b) - \frac{\pi b}{2}\big(J_1(b)H_0(b) - J_0(b)H_1(b)\big)\Big]\ }$$

(J = Bessel, H = Struve — a genuinely closed form in standard special functions.)
- **Derivation chain, machine-verified:** retarded resolvent of (d²/ds²+Ω²) → Γ(s)=∫dμ sin(√|t|εs)/√|t|·ε
  (ε=a₀/c); Laplace transform reproduces the master identity ∫dμ/(|t|+z) = 1−K(z) (the v11 structure);
  the Poisson representation of J₁ collapses the measure integral; region A+B combine into the single
  J₁/x tail integral.
- **Physical content:** Γ(0) = a₀/2c = 1/τ_mem exactly (the memory amplitude *is* the cut edge);
  ∫₀^∞Γ ds = 1 — **the v11 sum rule is the statement that the memory has unit total weight**;
  tail Γ ~ −τ_mem⁻¹√(2/π)·b^(−3/2) sin(b−3π/4): power-law (not exponential) memory with
  oscillation period 2πτ_mem ≈ 1275/1056 Gyr (canonical/alt) — τ_mem = 203/168 Gyr.
- **Flags:** EXACT given the published measure; convention z = c²□_u/a₀² (the one the docs' W=cω/a₀ uses).
  It is the kernel of the *operator* (Reading B) representation — reading-dependence inherited.
- **Novelty:** the framework's time-domain kernel has never been written anywhere (in-corpus grep +
  literature: nothing; MOND literature has no such object because standard MOND has no unique measure).
- **Utility:** enables direct time-domain/secular integrations (wide-binary, cluster-orbit, cosmological
  drift computations) without frequency-domain detours; any kernel deformation must keep ∫Γ=1.

### 4. E-S7-2/3 — THE THROTTLE LINE + a₀-LINE SATURATION (cluster closed forms) [N4 T3 D5* U4 = 16]
*(D5 given the Branch-B throttle postulate — POSTULATE-DEPENDENT, flagged)*

Above the kink (y > y_c = Z/2, depletion n=1), with D ≡ g_obs − g_bar:

$$\boxed{\ g_{\rm bar}\,D\,(D + Z a_0) \;=\; \tfrac{Z^2}{4}\,a_0^3\ \quad(\text{y-independent, zero-fit})}$$

and in the a₀-line plane (Y = g_obs²−g_bar² vs X = g_bar) the throttled framework is:
**Y = a₀X exactly below the kink; Y saturates to Y_∞ = (Z/2)a₀² = a₀·g_kink above it.**
General n: (g_obs−g_bar)·g_bar^n → y_cⁿa₀^(n+1)/2.
- **The kink location is a pure-Λ landmark** (credit: the g_bar = a₀V/2 statement is *already in* the
  y_c=Z/2 paper — Z cancels): g_kink = y_c a₀ = cH_Λ/2 = c²√(Λ/12), so **Λ = 12 g_kink²/c⁴** and
  H_Λ = 2g_kink/c — the broken-RAR kink is a direct Λ-meter with no a₀ and no Z in it.
  Numbers: 2.709×10⁻¹⁰ / 3.271×10⁻¹⁰ m/s² (canonical/alt; matches TARGET_SPEC).
- **Slope closed forms (new):** below, dln g_obs/dln g_bar = (2y+1)/(2(y+1)) → (Z+1)/(Z+2) = 0.8716 at
  y_c⁻; above (n=1) → [1−1/(Zν_c)]/ν_c = 0.7337, ν_c=√(1+2/Z); n=2 → 0.5958. Break invariants
  Δ = −0.1379 (n=1) / −0.2749 (n=2): **pure-Z, footing-free dimensionless numbers.**
  (Banked 0.872/0.734/0.597 reproduced; the 0.597 was a 3-digit coarse round of 0.5958.)
- **Peak landmark equation:** y* = 6.06 (n=1) / 5.24 (n=2), peaks 0.0170/0.0264 dex — matches the
  banked fingerprint; in g_bar: 5.7×10⁻¹⁰ (canonical).
- **Kink radius closed form (new):** Hernquist BCG ⇒ **r_kink = √(2GM_BCG/(cH_Λ)) − a_H**;
  9.4 kpc for M*=5×10¹¹ M⊙, R_e=12 kpc (TARGET_SPEC's 9.5 kpc reproduced to the gas correction).
- **Honesty:** Branch-B only (uncut MI has NO throttle); the y_c paper itself reports 0.5–0.6σ
  SPARC indistinguishability and TARGET_SPEC shows the cluster kink is not currently detectable
  (BCG M/L systematic 4–6×the signal). These are exact *target* equations, not detections.

### 5. E-S6-2/4/5 — THE PHANTOM HALO AND ITS PROJECTION: the (K,E) elliptic pair [N4 T4 D5 U4 = 17]

$$\rho_{\rm ph}(r) = \frac{\sqrt{GMa_0}}{4\pi G}\,\frac{1}{r\sqrt{r^2+r_M^2}}\ ,\qquad
\Sigma_{\rm ph}(b) = \frac{\sqrt{GMa_0}}{2\pi G}\,\frac{K(m)}{\sqrt{b^2+r_M^2}}\ ,\quad m=\frac{1}{1+u^2}$$

- The framework's "dark halo" of a point mass in closed form: an **inner 1/r cusp** (not NFW's, not
  cored) rolling to exact isothermal 1/r² at r ≫ r_M. Its projection is a complete elliptic K with the
  **same modulus m as the deflection's E** — deflection and convergence are one elliptic system, and
  the exact closure **dM₂D/db = 2πb Σ_ph** is machine-verified symbolically (sympy elliptic
  derivatives). Concept of MOND phantom density = Milgrom (credited; e.g. Milgrom 2008 rings/shells
  paper); the closed forms for THIS ν and the (K,E)-pair structure: not found in the literature.
- Testability: cluster/galaxy strong+weak lensing profile fits; the 1/r-cusp-to-isothermal shape is a
  falsifiable alternative template to NFW around isolated compact masses.

### 6. E-S2-1/2 — THE FLOOR-FORM INVERSION + the Milgrom-ΔT correspondence [N3 T4 D5 U4 = 16]

$$\boxed{\ g_{\rm bar} \;=\; \sqrt{g_{\rm obs}^2 + (a_0/2)^2}\; -\; a_0/2\ }\qquad
\Longleftrightarrow\qquad (2g_{\rm bar}+a_0)^2 - (2g_{\rm obs})^2 = a_0^2$$

- The exact inversion of the framework law is itself a **dS-Unruh temperature-excess**: the Newtonian
  source is the excess of the Pythagorean temperature over a floor at **a₀/2** — and a₀/2c is exactly
  the **branch point of the Herglotz measure** (region-A cut edge |t|=¼ ↔ ω_edge=a₀/2c). Thermal form:
  k_B[T_eff(g_obs;T_*)−T_*] = ħg_bar/(2πc), T_* = ħa₀/(4πck_B) = T_dS/(2Z).
- **CREDIT (novelty-checked):** the functional form [√(a²+κ²)−κ]/a *is* Milgrom 1999
  (Phys. Lett. A 253, 273, astro-ph/9805346 — "the modified dynamics as a vacuum effect",
  T ∝ √(a²+a₀²), ΔT ∝ MOND inertia). The framework kernel is EXACTLY that function with floor
  κ = a₀/2 — machine-verified. **Not a new function.** The new content is the two welds: (i) floor =
  the measure's cut edge (the thermal floor and the spectral gap are the same number), and (ii) the
  floor sits at cH_Λ/(2Z), i.e. **2Z ≈ 11.58 below the framework's own dS scale** — an honest
  structural tension to carry, not hide: the ΔT reading only closes with a floor 2Z under the horizon
  value the framework's own derivation would naively supply.
- The hyperbola form is algebraically the SAME identity as the a₀-line (verified: hyperbola ≡ −4×a₀-line)
  — value is the numerically-stable inversion (no catastrophic cancellation; use in any g_bar-from-g_obs
  estimator, e.g. the S1 baryon-mass predictor) and the thermal reading.

### 7. E-S2-3/4/5 — THE THERMAL a₀-LINE + welds [N3 T1 D5 U2 = 11]

(cκ_eff)² − (cH_Λ)² = g_bar² + a₀g_bar exactly (the a₀-line as a temperature-squared statement:
(2πck_B/ħ)²(T_eff²−T_dS²) = g_bar²+a₀g_bar); (T_eff/T_dS)² = 1 + y(y+1)/Z²;
**τ_mem·H_Λ = 2Z exactly** (the memory time is 2Z horizon times — footing-free; 203 Gyr vs 17.5 Gyr
canonical); κ_eff(a₀)/H_Λ = √(1+1/Z²) = 1.01481 (re-verified = PULLBACK.md). Exact but with Unruh
temperatures unmeasurable — consistency welds, not tests.

### 8. E-S4-2/3 — UNITARITY CIRCLE, PHASE-LAG LAW, SPECTRAL DICHOTOMY [N3 T2 D5 U2 = 12]

On bound orbits (cut boundary, W = cω/a₀ > ½): K = (√(4W²−1)+i)/(2W), **|K| = 1 exactly** — the
response is pure phase, φ(ω) = arcsin(a₀/2cω); reactive deficit 1−ReK = 1−√(1−sin²φ) ≈ ½(a₀/2cω)²;
drift identity 2ω·ImK = a₀/c (= laneK's universal secular drift, credited). **Dichotomy at the edge:**
ω > a₀/2c pure phase (|K|=1, zero amplitude response — the laneK kinematic suppression); ω < a₀/2c
purely dissipative boundary value (ReK=0, |K|<1→0). Wide-binary numbers: φ = 10⁻⁷–10⁻⁶ rad,
ṙ = 4–36 km/yr at 3–20 kAU — **flagged Reading-B**: the drift channel is already excluded ~250–500×
at planets (KERNEL_PLANETS.md), so these are exact consequences of the operator reading, not endorsed
phenomenology; under gated Reading C they are suppressed by the ~Myr corner.

### 9. E-S4-4 — THE INVERSE-MOMENT FAMILY (sum-rule generalization) [N4 T1 D5 U2 = 12]

$$M_p \equiv \int \frac{d\mu(t)}{|t|^p} \;=\; \frac{2^{2p-2}\,\Gamma(\tfrac{3}{2}-p)}{\sqrt{\pi}\,(2p-1)\,\Gamma(2-p)}\ ,
\qquad p\in(\tfrac{1}{2},\tfrac{3}{2})$$

M₁ = 1 recovers the v11 sum rule; region-B share 2/π re-derived; endpoints diverge exactly where they
must (p→½⁺ from the region-B tail, p→3/2⁻ from the cut edge — the same a₀/2c edge as E-S2-2).
A one-parameter fingerprint family: any future modification of the kernel must reproduce all M_p, not
just M₁. Theory-internal.

---

## HONESTY LEDGER
- **Both footings** carried in every dimensional number (canonical 9.362e-11 / alt 1.130e-10);
  Z-only results marked footing-free.
- **Exact vs approximate:** every boxed identity is EXACT under the stated premises; approximations
  are only in stated limits (approach law O(u⁻⁴); tail asymptotics) and are labeled.
- **Postulate flags:** S7 = Branch-B throttle postulate; S4 phase/drift/dichotomy = operator
  (Reading B) evaluation, which laneK showed is drift-excluded and RAR-erasing — carried verbatim;
  S6 = spherical/pinned + weak field + isolated (gap A inherited off-sphere; photon-timing LOS bound
  open per UNIFICATION P3); s=−1 and a₀'s value remain inputs everywhere.
- **Credits from novelty checks (WebSearch, 2026-07-16):** Milgrom 1999 astro-ph/9805346 (ΔT form);
  Mortlock & Turner 2001 astro-ph/0106100 (deep-MOND α_∞, piecewise point-lens forms); Milgrom
  phantom-matter concept (e.g. arXiv:0709.2561); the y_c=Z/2 paper's own a₀V/2 statement
  (ELASTIC_MEDIUM_YC_Z2_2026.md) for the kink location. Not found in literature: the elliptic-E
  deflection closed form, the (K,E) pair, the mass-line estimator form, the time-domain Γ(s), the
  M_p family, the throttle cubic invariant / a₀-line saturation, the floor≡cut-edge weld.
- **No numerology:** every equation derives from the action/premises; no digit hunts.
- **Data fire:** one (SPARC mass-line, read-only) — result NON-diagnostic between footings, as the
  banked audit requires; the WLS-bias methodological finding is the actionable output.
- Frozen repo untouched; all outputs in `prep_2026/equation_book/`.

## REPRODUCTION
```bash
cd /Users/carlzimmerman/new_physics/prep_2026/equation_book
python3 s2_thermal_identities.py     # exit 0, 12 checks
python3 s4_kernel_spectral.py        # exit 0, 44 checks
python3 s6_lensing_closed_form.py    # exit 0, 14 checks
python3 s7_throttle_closed_form.py   # exit 0, 22 checks
python3 m2_massline_sparc_fire.py    # exit 0, SPARC 175/3389 read-only
```
