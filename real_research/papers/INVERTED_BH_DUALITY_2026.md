# The Inverted Black Hole: Why the de Sitter–MOND Acceleration Scale Is Uniquely Cosmic

**Carl P. Zimmerman** · Briar Creek Tech · 2026-06-26

---

## Abstract

The MOND acceleration scale can be written exactly as a horizon surface gravity divided by a single dimensionless constant:

> **a₀ = c²√(Λ/32π) = cH_Λ / Z,  Z = 2√(8π/3) = √(32π/3) ≈ 5.789.**

The de Sitter horizon that supplies cH_Λ is, geometrically, an **inverted black hole** — a horizon we sit *inside* rather than outside. This note takes that picture literally and asks what happens when the same law, *a₀ = (horizon surface gravity)/Z*, is applied to a **real** black-hole horizon instead of the cosmic one. The dual is clean and exact: **a₀_BH = c⁴/(4GMZ)**, and the radius at which it would switch on, **r_cross = √Z · r_s = 2.406 r_s, is universal — the black-hole mass cancels completely.** For Sagittarius A\*, M87\*, and a 10 M_⊙ stellar black hole this crossover sits at the same place in units of the Schwarzschild radius, between the photon sphere (1.5 r_s) and the ISCO (3 r_s).

We show that this dual nonetheless **self-cancels into pure general relativity** for every clean observable, for two structural reasons — mass-independence (any deviation expressed as f(r/r_s) is already inside the GR metric by general covariance and the equivalence principle) and the free-fall / Hartle–Hawking theorem (a geodesic observer sees no horizon bath, and modified inertia responds only to *proper* acceleration). We explicitly reject the naïve "g ≫ a₀ near a horizon, so the effect vanishes" objection: it is **false**, because a₀_BH scales up with c⁴/GM identically, keeping the ratio a/a₀_BH of order unity right down to the horizon. The effect does not trivially vanish; it cancels for a precise and instructive reason.

This singles out a **uniqueness proposition**: the cosmic a₀ is the *only* acceleration that is neither sourced by local matter nor removable by any local free-fall — which is exactly why a₀ is cosmic and not, say, set by the nearest black hole. The one falsifiable residue is a **null**: the modified-inertia reading forces *exactly-GR* shadows, ISCO frequencies, ringdown spectra, and inspiral waveforms, whereas a metric completion that genuinely *shifts the black-hole metric* — MOG / Scalar-Tensor-Vector is the clean example — predicts shifted strong-field observables. (The framework's own host theory, AeST, is *not* such a rival: its published black holes are *stealth*, with exactly-GR geometry [Skordis & Złośnik, arXiv:2412.15395], so it shares the framework's null — the test is sharp against metric-shifting theories like MOG, not against AeST.) A future ngEHT or LISA detection of a MOND-scale black-hole-metric deviation would therefore **falsify a metric-shifting completion such as MOG while being consistent with this framework**.

Both ways: this is a *structural duality and a null*, not a new force, not a new positive signal, and not a theory of everything. Its only discriminating axis is modified-inertia-versus-modified-gravity — the same axis as the existing Cassini bound, extended to the strong field — and it is decadal. It claims **less**, not more, than the framework's published one-parameter effective theory (DOI [10.5281/zenodo.20935948](https://doi.org/10.5281/zenodo.20935948), [10.5281/zenodo.20938891](https://doi.org/10.5281/zenodo.20938891)) and is fully consistent with the author's 2026 retraction of the earlier theory-of-everything overclaims.

---

## 1. Background: the de Sitter horizon as an inverted black hole

### 1.1 The acceleration scale as a horizon surface gravity

The empirical MOND scale a₀ ≈ 1.2×10⁻¹⁰ m s⁻² is the acceleration below which galaxy rotation curves flatten. The framework's single physical claim is that this scale is *cosmological in origin* and equals a de Sitter horizon surface gravity reduced by one geometric factor:

$$a_0 \;=\; \frac{c\,H_\Lambda}{Z}, \qquad H_\Lambda \equiv c\sqrt{\Lambda/3}, \qquad Z = 2\sqrt{8\pi/3}\approx 5.789.$$

Here Λ is the cosmological constant and H_Λ = H₀√Ω_Λ is the de Sitter (dark-energy-only) expansion rate, numerically 1.807×10⁻¹⁸ s⁻¹ (H₀ = 67.4 km s⁻¹ Mpc⁻¹, Ω_Λ = 0.685), giving a₀ = 9.36×10⁻¹¹ m s⁻² — the framework's published value. The quantity cH_Λ is the **surface gravity of the de Sitter horizon**: just as a black hole of mass M has a horizon at the Schwarzschild radius r_s = 2GM/c² with surface gravity κ_BH = c⁴/4GM, de Sitter space has a cosmological horizon at radius r_dS = c/H_Λ with surface gravity κ_dS = cH_Λ. Both are accelerations; both set a Hawking/Unruh temperature T = ħκ/2πk_Bc. The number Z = √(32π/3) is algebraically forced — it is the Einstein coupling 8π (from ρ_DE = Λc²/8πG) times the Friedmann 3 (from H² = 8πGρ/3), with a single free outside factor of 2. (The closure of *that* coefficient is the subject of a companion note; here we treat Z as fixed and ask about its application to real horizons.)

### 1.2 Why "inverted"

A Schwarzschild black hole is a horizon seen **from outside**: matter is concentrated at the center, the horizon surrounds it, and surface gravity *increases* as the mass increases — or, for fixed mass, as you fall *inward*. The de Sitter horizon is the same geometry turned inside-out. We sit *inside* it; the "concentration" is the vacuum energy filling all space; the horizon is the sphere at comoving distance c/H_Λ beyond which recession exceeds c; and surface gravity is felt looking *outward*. Formally, the static de Sitter metric

$$ds^2 = -\left(1 - \frac{r^2}{r_{dS}^2}\right)c^2dt^2 + \left(1 - \frac{r^2}{r_{dS}^2}\right)^{-1}dr^2 + r^2 d\Omega^2$$

is the Schwarzschild metric with the sign of the curvature term flipped and the mass term replaced by the Λr² term — a black hole inverted in both the location of the horizon (far, not near) and the sign of the potential. This is not loose analogy: de Sitter and Schwarzschild are the two limits of the Schwarzschild–de Sitter family, and a₀ = κ/Z is one law evaluated on the two horizons. The framework's content is that **inertia is the response to the bath of the inverted (cosmic) horizon**, and the natural test of that idea is to evaluate the *same response* on a real horizon.

---

## 2. The dual: a₀_BH = c⁴/(4GMZ) and the universal crossover

Apply *a₀ = (surface gravity)/Z* to a Schwarzschild horizon, κ_BH = c⁴/4GM:

$$\boxed{\,a_{0,\mathrm{BH}} = \frac{\kappa_{\mathrm{BH}}}{Z} = \frac{c^4}{4GMZ}\,.}$$

Numerically (verified in mpmath, dps = 40):

| Black hole | Mass | a₀_BH (m s⁻²) | ratio to cosmic a₀ |
|---|---|---|---|
| Sagittarius A\* | 4.3×10⁶ M_⊙ | 6.11×10⁵ | 6.3×10¹⁵ |
| M87\* | 6.5×10⁹ M_⊙ | 4.04×10² | 4.2×10¹² |
| Stellar (10 M_⊙) | 10 M_⊙ | 2.63×10¹¹ | 2.7×10²¹ |

Every real horizon is 12–21 orders of magnitude "hotter" than the cosmic one — unsurprising, since cosmic a₀ is the gentlest acceleration in nature.

**The crossover radius is universal.** Modified inertia switches regime where the Newtonian acceleration g(r) = GM/r² equals the local scale a₀_BH:

$$\frac{GM}{r^2} = \frac{c^4}{4GMZ}\;\Longrightarrow\; r_{\mathrm{cross}}^2 = \frac{4G^2M^2 Z}{c^4} = Z\,r_s^2,\qquad \boxed{\,r_{\mathrm{cross}} = \sqrt{Z}\,r_s = 2.406\,r_s\,.}$$

**Why the mass cancels.** g(r) = GM/r² carries one power of M; a₀_BH = c⁴/4GMZ carries one *inverse* power of M. Setting them equal makes M² appear on both sides and cancel, leaving a pure number times r_s² — and r_s itself is the only length the problem contains. So r_cross is the same multiple of r_s for a stellar black hole and for M87\*: **2.406 r_s, always.** It sits between the photon sphere (1.5 r_s) and the ISCO (3 r_s). The dimensionless acceleration at the ISCO is likewise mass-free and O(1): x_ISCO = a/a₀_BH = Z/9 = 0.643 on the Newtonian reading (≈ 0.79 including the proper-acceleration/redshift factor). For *every* black hole, the MOND regime would, naïvely, bite right in the observationally active band of photon ring, ISCO, and ringdown.

---

## 3. The self-cancellation: why it is nonetheless pure GR

### 3.1 First, kill the lazy objection

A common reflex is: "near a black hole g is enormous, so g ≫ a₀, so we are deep in the Newtonian/GR regime where the MOND interpolation μ → 1 and nothing changes." **This is false, and we reject it explicitly.** It silently uses the *cosmic* a₀ as the yardstick. But the relevant scale here is the black hole's *own* a₀_BH, which scales up as c⁴/GM in lockstep with g. Their ratio x = a/a₀_BH is set entirely by r/r_s and stays O(1) (indeed 0.6–0.8) right down to the horizon, as §2 shows. So the effect does **not** trivially vanish near the horizon. Something subtler is going on.

### 3.2 First reason it cancels: mass-independence ⇒ already inside the GR metric

The tell is precisely that r_cross = 2.406 r_s and x_ISCO = 0.643 depend *only* on r/r_s. The scale a₀_BH = κ_BH/Z is built from c⁴/GM — a pure general-relativistic quantity, the horizon surface gravity, which the Schwarzschild metric already contains. Any "modification" expressible as a function f(r/r_s) carries no information the metric does not already have, so by **general covariance plus the equivalence principle** it is absorbed into the geodesic motion GR already prescribes. A correction that is a function of the metric's own invariants is not a new force; it is a re-labeling of GR. This is the structural opposite of the cosmic case, where a₀ ∝ √Λ introduces a scale *external* to the local two-body metric.

### 3.3 Second reason it cancels: the free-fall / Hartle–Hawking theorem

The framework's inertia is sourced by **proper** acceleration — the acceleration a body feels relative to its local inertial frame, the thing an accelerometer reads. A freely-falling (geodesic) detector near a black-hole horizon reads **zero**, and by the standard Hartle–Hawking / Unruh–DeWitt result it sees **no Hawking or Unruh bath**: the Hartle–Hawking vacuum is regular on the horizon precisely for the freely-falling observer. Orbits, photon trajectories, inspiraling binaries, and the ringing of the final black hole are all **geodesic** phenomena. A geodesic observer has no proper acceleration for the modified-inertia response to act on, and no bath to respond to. Therefore a₀_BH touches **no geodesic observable**: the ISCO frequency, the quasinormal-mode (ringdown) spectrum, the photon ring and EHT shadow, the gravitational-wave inspiral, and QPO frequencies are all **exactly GR**, with no a₀_BH correction.

The one non-geodesic loophole is genuinely accelerated matter — accretion-disk and jet plasma held off geodesics by pressure and magnetic stress. But there the dynamics are completely swamped by magnetohydrodynamics and radiation pressure, whose forces dwarf any a₀_BH-scale inertial correction by many orders of magnitude. It is not a clean test, and we do not claim one.

---

## 4. The uniqueness proposition: why a₀ is cosmic

Sections 2–3 deliver more than a null. They isolate **what is special about the cosmic horizon** by showing what fails for every other horizon. State it sharply. An acceleration scale can imprint a *physical*, non-removable modified-inertia effect only if it is:

1. **not sourced by local matter** — otherwise it is a function of the local metric's invariants (here f(r/r_s)) and is absorbed into the GR geodesic by covariance + EP (§3.2); and
2. **not removable by local free-fall** — otherwise a geodesic observer transforms it away and sees no bath, by the Hartle–Hawking theorem (§3.3).

A real black-hole horizon fails **both**: its surface gravity is a local-metric quantity, and its bath is absent for the geodesic observers who execute every clean strong-field measurement. The cosmic acceleration cH_Λ fails **neither**. It is not sourced by any local mass — it is set by Λ, a global vacuum property, the same everywhere — so it is *not* a function of any two-body r/r_s and cannot be covariantly absorbed. And it cannot be removed by free-fall over a bound system, because **there is no global inertial frame that straightens out de Sitter expansion over a Hubble volume**; a freely-falling galaxy still recedes from the horizon. The de Sitter horizon supplies a genuine, irreducible acceleration *floor* that a bound orbit cannot transform away, whereas a black-hole horizon supplies none for the orbit around it.

**This is why a₀ is cosmic.** It is not a coincidence of magnitude that the modified-inertia scale matches √Λ rather than the surface gravity of the nearest or largest black hole. The cosmic horizon is the **unique** horizon whose acceleration is neither local-matter-sourced nor free-fall-removable — and uniqueness is exactly the property a fundamental, universal scale must have. The dual to real black holes is the proof: run the same law on every other horizon and it cancels; only the inverted, cosmic horizon survives.

---

## 5. The falsifiable consequence: an exactly-GR null

The framework therefore makes a sharp, *forced* prediction at the strong-field scale that none of its previously banked tests reach:

> **Null prediction.** The modified-inertia reading predicts **exactly-GR** black-hole shadows, photon spheres, ISCO frequencies, ringdown quasinormal-mode spectra, and inspiral–merger waveforms for Sagittarius A\*, M87\*, and stellar-mass black holes, with **no a₀_BH correction whatsoever.**

The discriminating power is real but narrow, and it is a **falsification asymmetry**, not a positive signal. Crucially, it separates theories not by the label "MOND" but by whether their black holes carry a **non-stealth metric shift**:

- **MOG / Scalar-Tensor-Vector (the clean rival).** MOG genuinely modifies the black-hole metric: the effective mass becomes M → M(1+α), enlarging the shadow by ≈ +α and shifting the ISCO frequency by ≈ −α (per unit α, near the GR limit). The Event Horizon Telescope already bounds α < 0.044 for Sgr A\* and α ≈ 0.04–0.23 for M87\*; ngEHT (shadow fidelity ~2–5%, 2030s) probes α ~ 0.02–0.05, and LISA ringdown spectroscopy (2035+) reaches α ~ 0.006. Since r_cross = 2.406 r_s lands squarely in the photon-ring / ISCO band, such a shift is in the observable window. A clean GR-consistent measurement falsifies horizon-scale MOG.
- **AeST / Aether-Scalar-Tensor (the framework's own host) is *not* a rival on this axis.** AeST admits **stealth** black holes whose background metric is *exactly* a GR solution (Reissner–Nordström for the physical q = 1 case), carrying only secondary hair (Skordis & Złośnik, arXiv:2412.15395). Every geodesic observable — shadow, photon sphere, ISCO frequency, inspiral — is therefore **GR-identical in AeST**; the authors note that only an uncharacterized, sub-percent quasinormal-mode / thermodynamic channel could differ, which is below ngEHT/LISA reach. So the shadow/ISCO/ringdown test is **null-vs-null between this framework and AeST** — it does *not* distinguish them. (Independently, the AeST MOND scalar length c²/a₀ ≈ 10²⁷ m sits ~17 orders of magnitude above any black-hole horizon, so the scalar is screened there regardless.)
- This framework, being a modified-*inertia* theory with a **standard GR metric**, predicts no shift — the *same* null as AeST's stealth branch.

Hence a future detection of a MOND-scale black-hole-**metric** deviation would **falsify a metric-shifting completion such as MOG, while being consistent with — indeed predicted by — both this framework and AeST's stealth black holes**; a confirmed pure-GR shadow/ringdown is a (weak) consistency point for the inertial reading that does *not* separate it from AeST. The relevant instruments are **ngEHT** (next-generation Event Horizon Telescope: M87\* and Sgr A\* shadows to ~1–2%, 2030s) and **LISA / LIGO-Virgo-KAGRA** ringdown spectroscopy plus LISA EMRI and massive-black-hole inspirals (2035+).

**Both ways — the honest limits.** (i) It is a **null**, not a detection: no positive signal can be claimed, only a falsification asymmetry. (ii) Its only axis is **modified-inertia-versus-modified-gravity**, the *same axis* as the framework's existing Cassini bound — it **extends Cassini to the strong field** rather than opening an independent axis. (iii) It is **decadal-plus** and at a precision (~1–2%) that may sit below the level at which a MOND-scale metric shift would even appear. So it does not supersede the framework's two sharpest near-term fronts (a declining a₀(z) tested via the baryonic Tully–Fisher sign, and a Lorentz-violating s^TX SME dipole); it is weaker and farther than either. It is a real new consequence, reported at its true strength.

---

## 6. Scope: a structural duality and a null — claiming less, not more

To be explicit about what this is and is not:

- It is a **structural duality** (a₀_BH = c⁴/4GMZ with the universal r_cross = 2.406 r_s) plus a **forced null** (exactly-GR strong-field observables). Both follow rigorously from the published law a₀ = κ/Z and from textbook results (Hartle–Hawking regularity, covariance + EP). No new postulate is introduced.
- It is **not a new force**, **not a new positive signal**, and **not a theory of everything**. It introduces **no new free parameter**: a₀_BH is fixed by the *same* Z and the black hole's GR mass.
- It is **fully consistent with**, and supplements, the framework's published one-parameter effective theory (DOI [10.5281/zenodo.20935948](https://doi.org/10.5281/zenodo.20935948), [10.5281/zenodo.20938891](https://doi.org/10.5281/zenodo.20938891)) and with the author's 2026 public retraction of the earlier Standard-Model / theory-of-everything overclaims. If anything it **strengthens** the modest reading: it explains, via the uniqueness proposition, *why* the single physical scale is cosmic, and it adds a strong-field falsification handle on *metric-shifting* rival theories such as MOG — though *not* on the framework's own host theory AeST, whose published stealth black holes share the framework's exactly-GR null — without adding anything the framework must itself defend.

The net contribution is one new, narrow, far, **null** consequence — the BH-scale exactly-GR prediction — and a clean reason it is a null. Taken together with the duality and the uniqueness proposition, the result tightens the conceptual case for a cosmic a₀ while making no claim the data cannot, in time, check.

---

## Reproducibility note

All numerical statements (a₀ on the framework footing; a₀_BH for Sgr A\*, M87\*, and a 10 M_⊙ black hole; r_cross = √Z r_s = 2.406 r_s; x_ISCO = Z/9 = 0.643; Z = √(32π/3) = 5.78881) were verified in mpmath at 40-digit precision. The crossover-radius derivation (mass cancellation) and the ISCO ratio are one-line algebraic identities reproducible from the public repository. The free-fall / no-bath statement is the standard Hartle–Hawking / Unruh–DeWitt result for a geodesic detector; the covariance + equivalence-principle absorption argument is qualitative and stated as such. The underlying consequence map (`real_research/FRONTIER_CONSEQUENCES_INVERTED_BH_2026-06.md`) records the full both-ways analysis, including the parallel finding that taking the de Sitter–Unruh bath as physically real yields a deep-vacuum bath (T_dS = 2.28×10⁻³⁰ K) with no laboratory decoherence or quantum-modified-inertia signature — a defensive null reported there at its true (below-floor) strength.

---

*Carl P. Zimmerman · Briar Creek Tech · 2026-06-26. This work claims a structural duality and a falsifiable null, consistent with and supplementing the author's published one-parameter effective theory; it does not claim a new force or a theory of everything.*
