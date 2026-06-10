# Door I (mechanism test for F4): the λ² worldline back-reaction REFUTES the susceptibility structure in the adiabatic channel — and a contraction census extends the no-go to all finite orders

*agentB, 2026-06-10. Task: does a first-principles λ² calculation SUPPORT, REFUTE, or leave OPEN the F4 hypothesis
(inertia = susceptibility of the UDW detector's thermal state to acceleration, m_eff ∝ dT_eff/da, T_eff the
Deser–Levin temperature, giving μ(x) = x/√(1+x²) parameter-free)? Artifacts: `agentB_door1_static_kernel.py` +
`.out` (sympy identities machine-verified two independent ways; mpmath numerics cross-checked by two routes to
9 digits). Verdict at the end, both ways. Units ħ = c = k_B = 1 except where restored.*

## STAGE 0 — flat-space sanity anchor (required): PASSES, and is exactly how F4 degenerates
T_eff = (1/2π)√(a² + H²) ⇒ dT_eff/da = (1/2π)·a/√(a²+H²). As H → 0 this → 1/2π = dT_U/da = constant
(restored: ħ/2πck_B), i.e. m_eff ∝ const: **ordinary inertia**, for every a > 0. The normalization is
self-fixing because the flat-space susceptibility is the constant ħ/2πck_B:
μ(x) ≡ (dT_eff/da)/(dT_U/da)|_flat = x/√(1+x²), x = a/cH. Order of limits noted: a→0 at fixed H gives μ→0
(deep MOND); H→0 at fixed a gives μ→1 (ordinary). Stated, verified, trivial — as required.

## STAGE 1 — literature anchor for bath back-reaction at λ² (required): pinned
- **Einstein–Hopf class** (arXiv:1112.5195, Lach/Jentschura et al., unifying review): an atom moving with
  velocity v through thermal radiation feels F = −γv with
  **γ ∝ ∫₀^∞ dω ω⁵ (∂n(ω,T)/∂ω) Im α(ω)** (n = thermal occupation, α = polarizability); the original
  Einstein–Hopf 1910 oscillator form is F = (ħe²ω₀⁴v)/(15πmc³ε₀)·(∂n(ω₀;T)/∂ω₀) (sign opposing v).
  Structural lesson: the derivative that appears at λ² is **spectral** (∂n/∂ω at fixed state), never
  **parametric** (∂T/∂a).
- **Davies–Unruh bath drag** (arXiv:1205.0258, Kolekar & Padmanabhan): a particle with drift velocity in the
  Unruh bath feels F = −γ(E)v at linear response, with explicit gap- and temperature-dependent
  γ_∥, γ_⊥ (β = 2π/T; γ_x ∝ βE³e^{−βE}/(1−e^{−βE})²·[1 − 2/βE + 2e^{−βE}/βE + 2π²/β²E²], transverse
  analogue differs) — anisotropic, λ²-class, thermal-VALUE-dependent.
- **Force on a uniformly accelerated detector** (arXiv:1805.02888, Usenko & Lev, influence-functional):
  the vacuum back-reaction on a uniformly accelerated detector is "a force that inhibits the detector …
  proportional to the acceleration of the leading center," compensated by the external agent — i.e. at the
  stationary level the back-reaction is **inertia-renormalizing**, matching our key identity below.
- **dS consistency**: BD-vacuum thermalization of geodesic dS detectors at T_GH is standard (e.g.
  arXiv:1101.5235); dS-boost invariance maps geodesics to geodesics, so geodesic motion feels no drag —
  reproduced in our formulation by the exact prefactor a in the static force (zero at a = 0).

## STAGE 2 — the object: linear response about the stationary accelerated dS worldline
**Setup** (meets F4 on the family's own terms): conformally coupled massless scalar in dS₄, Bunch–Davies
(this IS the repo's banked Γ_th machinery: the comoving pullback −(H²/16π²)/sinh²(HΔτ/2) is its a = 0 case);
point monopole UDW detector, H_int = λμ̂(τ)φ(z(τ)), gap Ω. Embedding X·X = 1/H² in 5D Minkowski; the
uniformly accelerated worldline is X(τ) = (κ⁻¹sinh κτ, κ⁻¹cosh κτ, a/Hκ, 0, 0), **κ = √(a²+H²)**, with
orthonormal frame relations u̇ = aê + HN, ê̇ = au, Ṅ = Hu (ê = acceleration direction, N = HX the normal).
All machine-verified (`.out` [A1]).

**Exact pullbacks** (machine-verified, [A2]–[A6]):
1. Z(s) = (H²cosh κs + a²)/κ², 1−Z = −(2H²/κ²)sinh²(κs/2) ⇒ W(s) = (H²/8π²)/(1−Z) =
   **−(κ²/16π²)/sinh²(κ(s−iε)/2)** — the Deser–Levin thermal form at T_eff = κ/2π, exactly.
2. **KEY IDENTITY:** the longitudinal gradient pullback obeys **ê·∇W(s) = −a·W(s) exactly**
   (independently re-derived in flat 4D Rindler coordinates with no embedding, [B1–B2]).
3. **SECOND IDENTITY:** the longitudinal force-force kernel decomposes exactly as
   **K_FF(s) ≡ ê^Aê'^B∇_A∇'_B W = K_⊥(s) + a²W(s)**, K_⊥ = κ⁴/(32π²)sinh⁻⁴(κ(s−iε)/2)
   (at a = 0, longitudinal = transverse: isotropy check ✓).

**The static (adiabatic) force.** In-in at O(λ²): ⟨f(τ)⟩ = −2λ² Im ∫₀^∞ ds g(s)·ê·∇W(s) with
g(s) = ⟨μ̂(s)μ̂(0)⟩. By identity (2):
> **⟨f_rad⟩ = −a · λ²[δm_UV + G_th(κ, Ω, state)]** — exactly ordinary-inertia form. The geometric
> projection supplies exactly one factor a; everything else is a function of κ (= of T_eff) and Ω only.

δm_UV is the κ-independent flat-vacuum mass renormalization (gapless case: Im∫₀^∞W ds = −1/4π²ε + O(ε),
finite part **exactly zero**); G_th is the finite thermal mass, computed two independent ways (time-domain
quadosc vs PV-spectral, agree to 9 digits, [D1]): G_th = 2∫₀^∞ sin(Ωs)[W_κ(s) − W_vac(s)]ds, with
- low-T (κ≪Ω): G_th → λ²T_eff²/(6Ω) (the classic thermal shift; coefficient verified, [D2]);
- gapless (Ω→0): G_th → 0 like Ω·ln — **no induced structure at all** in the universal/gapless channel [D3];
- high-T: G_th ≈ (Ω/2π²)[ln(κ/Ω) + O(1)] (log-slope = 1/2π² to 0.1%, the banked Γ_th coefficient family) [D4];
- positive in all probed regimes and **growing with κ**: the bath ADDS inertia with temperature;
- equilibrated (Gibbs at T_eff) detector: thermal part is odd in Ω ⇒ G_eq = tanh(πΩ/κ)·G_th — still
  (κ,Ω)-only [D6] (mean-force/Kubo subtleties of the thermal-detector vacuum cross-term flagged for the
  handoff; they cannot change the (κ,Ω)-only structure).

**The adiabatic acceleration-conjugate kernel.** For slow δa(τ), the response is the quasi-static walk
through the stationary family: δ⟨f⟩ = −m_resp(a)·δa with
**m_resp(a,H) = G(κ) + (a²/κ)G′(κ)** (plus the bare/UV constant). THE QUESTION's answer:
> **NO — m_resp is NOT ∝ dT_eff/da.** Demanding G + (a²/κ)G′ = C·a/(2πκ) forces
> **G(κ) = [Cκ/2 + πc₁]/(π√(κ²−H²))** ([C1], sympy dsolve): every solution depends explicitly on H and has
> a **pole at κ = H, i.e. exactly at a = 0 — the deep-MOND limit**. But G is built solely from the κ-thermal
> worldline correlators and cannot know H separately. No such G exists unless C = 0, and C = 0 is ordinary
> (constant) inertia. The numerics make it vivid ([D5]): m_resp has a NONZERO floor at a→0 (the thermal mass
> at T_dS) and grows without bound in a, while μ_F4 must vanish at a→0 and saturate at 1.

**Census extension (the strongest statement).** By identity (3) the entire anisotropy of the λ² problem is
the single term a²W(s); the redshift/clock contact vertices likewise carry a×(one ê-factor a) = a². Hence
**every λ² response coefficient — static, drag γ(ω), or ω²-inertia, longitudinal or transverse — has the
form A(κ,Ω) + a²B(κ,Ω)**; at order λ^{2n}, a polynomial of degree n in a² with κ-only coefficients. μ_F4 =
a/κ = √(κ²−H²)/κ is non-polynomial in a² (non-linear in H² at fixed κ) ⇒ **excluded at every finite order
in λ**. The susceptibility structure, if it has a mechanism here at all, must be non-perturbative (note the
suggestive alignment: perturbation theory in λ is exactly what must fail if induced inertia is to *vanish*
at a→0) or live outside this model class.

**What WOULD have supported F4** (both-ways): a renormalized kernel ∝ a/κ, vanishing at a = 0, saturating at
high a. What we found instead: a **thermal-mass dressing of ordinary inertia**, δm(T_eff) — finite at a = 0,
increasing with T_eff, i.e. curvature in the **anti-MOND** direction (deep MOND needs an inertia *deficit*).
This is a kill in the pre-registered Door-I sense ("if the drag kernel lacks the susceptibility structure
(wrong sign/shape) → F4 loses its mechanism candidacy") for the adiabatic channel and, by the census, for
all finite-order λ channels of this model class.

**The exact remaining integral (the honest handoff — what is NOT closed).** The full frequency-dependent
kernel about the stationary orbit:
> δ⟨f(τ)⟩ = ∫_{−∞}^τ dτ′ K(τ−τ′)ξ(τ′),
> **K(s) = 2λ²θ(s) Im{ g(s)[K_⊥(s−iε) + a²W(s−iε)] } + R(s)**,
> W(s) = −κ²/(16π²)sinh⁻²(κ(s−iε)/2), K_⊥(s) = κ⁴/(32π²)sinh⁻⁴(κ(s−iε)/2),
> g(s) = P_g e^{−iΩs} + P_e e^{+iΩs} (Gibbs at T_eff), and R(s) = the redshift-vertex terms
> [δ(dτ′) = aξdτ′ measure vertex paired with the force vertex ⇒ −2λ²a²θ(s)Im{g(s)W(s)}; the detector-clock
> shift δH_det = aξΩμ̂⁺μ̂; the instantaneous ⟨μ̂ ê·ê:∇∇φ⟩δ(s) term and its UV subtraction at κ→0].
> Contour: poles at s = 2πin/κ, n ≥ 1, iε below the real axis; χ(ω) = ∫₀^∞ds e^{iωs}K(s);
> γ(ω) = Im χ/ω (drag; consistency requirement γ→0 for geodesic-family perturbations at a = 0);
> δm₂ = −½ d²Reχ/dω²|₀ after the κ→0 subtraction (the ω²-inertia).
These integrals are digamma-class (same residue family as the banked Γ_th audit) and are worth computing for
Door IVa (eccentric-orbit/finite-frequency phenomenology) — but by the census above their coefficients are
A(κ)+a²B(κ) and **cannot rescue F4's a/κ**; they are no longer the deciding object for Door I.

## STAGE 3 — coefficient pre-registration (Door III): RAW NUMBERS FIRST
Raw, in isolation, exactly as produced ([.out] footer):
1. geometric prefactor in f_rad = −a·λ²G: **exactly 1**
2. gapless static finite part: **exactly 0**
3. low-T induced thermal mass: G_th = λ²T_eff²/(6Ω): **coefficient 1/6**
4. high-T log-slope of G_th: **1/(2π²)** (0.050610 measured vs 0.050661)
Post-hoc comparison (labeled as such): none equals Z = √(32π/3) = 5.789, 2, or 2π. Noted for honesty: 1/6 =
0.1667 sits 3.5% from 1/Z = 0.1727 — a numerical near-miss with zero structural significance (it is the
standard thermal-shift coefficient, multiplies the detector-dependent quantity T_eff²/Ω, and is not an a₀
coefficient); recorded so nobody "discovers" it later. Nothing was tuned; nothing lands on Z. The Door-III
hope (a λ² coefficient forcing ≈1/Z in the a₀ relation) did not materialize — consistent with the banked
verdict that Z is data-selected.

## PRIORITY SEARCH (required): no prior statement of "inertia ∝ dT_DL/da" found
Searched (web, multiple phrasings): Milgrom's vacuum papers and reviews; Smolin; Verlinde-adjacent/entropic;
"MOND Unruh susceptibility/temperature derivative"; McCulloch; Deser–Levin+MOND combinations.
- **Milgrom astro-ph/9805346** (Phys. Lett. A 253, 273): temperature-DIFFERENCE form only (repo-verified
  earlier; reconfirmed). His own pedagogical review (astro-ph/0112069 lineage) calls the difference form
  "the only explicit theoretical/heuristic derivation of μ" — strong indirect evidence the derivative form
  is not in his corpus.
- **Smolin arXiv:1704.00780**: regime/threshold argument (T below T_dS; weakened equivalence principle) —
  not dT/da.
- **McCulloch (e.g. arXiv:1610.06787)**: m_i = m(1 − 2c²/|a|Θ) — horizon-cutoff DIFFERENCE-type with a
  **linear 1/a tail** (ephemeris-exposed, F1-adjacent class), not dT/da.
- **Entropic class** (Verlinde 1611.02269; Pazy arXiv:1302.4411; Klein arXiv:1104.2022): screens/minimum
  temperature/dof-freezing — modified gravity-side, not worldline dT/da.
- **Darabi arXiv:0908.4239**: Mach/Unruh-like, gravitational-mass modification — not dT/da.
- Targeted phrase searches ("derivative of the Unruh temperature", "temperature susceptibility" + inertia,
  μ = x/√(1+x²) + Deser–Levin) returned **no hit** for m_eff ∝ dT_eff/da or μ_standard = d√(1+x²)/dx.
**Outcome: absence after a genuine multi-angle search** — F4's susceptibility reading appears to be novel
(with the standard caveat that web absence is not an exhaustive literature proof). Ironic counterpoint now
on record: the one-line identity is novel-looking, and the first first-principles test of it (this doc)
refutes it as a λ² worldline mechanism.

## VERDICT (both ways, full weight)
- **REFUTES** — in the precise sense Door I posed: at order λ² (and, by the contraction census, at every
  finite order in λ) for the monopole UDW detector + conformal massless scalar in dS₄ — the framework's own
  banked machinery — the adiabatic acceleration-conjugate response kernel is **m_resp = G(κ) + (a²/κ)G′(κ)**,
  a thermal-mass structure ∝ values of T_eff, with a nonzero a→0 floor and anti-MOND growth; it is **not**
  ∝ dT_eff/da, and no κ-only G can fake it (exact ODE no-go with a pole at the deep-MOND point). F4 loses
  λ²-mechanism candidacy per the pre-registered kill condition. This is a theory-side result: no footing,
  Υ, weighting, or a₀ convention enters anywhere.
- **What survives untouched**: F4 as a *selected effective law* (Saturn ×4 margin, SPARC competitive, DR4
  fork) — kill-test selection never claimed a mechanism; the kernel a₀ ∝ √ρ_DE; the difference-family
  no-gos. The Bohr-rule analogy sharpens: the rule stands, and its first candidate mechanics is now dead.
- **OPEN (named, honest)**: (i) non-perturbative/strong-coupling regime — the census blocks every finite
  order, and deep MOND (vanishing inertia) is exactly where perturbation theory around m_bare must fail;
  (ii) the minimally coupled massless scalar, whose dS IR pathology breaks the Deser–Levin κ-reduction —
  the one field choice where the no-go's premise fails; (iii) composite/multi-gap detectors and field-level
  (covariant, Door II) realizations — outside the worldline class entirely. The remaining integral above is
  well-posed for Door IVa regardless.
