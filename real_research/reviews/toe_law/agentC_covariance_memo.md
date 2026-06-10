# Door II — Covariance for the susceptibility coupling (F4): obstruction, loophole, or open?

*Agent C memo, 2026-06-10. Question (TOE_STATUS_AND_DOORS Door II): is covariantizing the F4 worldline rule
(m_eff ∝ dT_eff/da, T_eff the Deser–Levin temperature, equivalently μ_standard(x)=x/√(1+x²), x=a/cH) provably
obstructed, or is there a published loophole class? Method: literature audit pinned to arXiv ids + structural analysis.
Both-ways discipline applied: one finding here weakens the repo's strongest sentence (the trilemma perimeter), one
strengthens the MI cell (a 2026 Cassini result), and two new walls constrain F4's covariant ambitions. All reported at
full weight. C1/C2 only.*

---

## VERDICT (three layers, stated up front)

1. **NO OBSTRUCTION THEOREM exists, and one cannot be assembled from the audited parts.** Every candidate obstruction in
   the chain (Milgrom-94 nonlocality, the equivalence-principle/local-flatness argument, the Soussa–Woodard lensing
   no-go, the Bruneton–Esposito-Farèse singular surface) has a *published, named evasion*. The chain terminates in an
   existing theory class, not a no-go.
2. **LOOPHOLE — for the law rung as a whole.** The nonlocal pure-metric class (Deffayet–Esposito-Farèse–Woodard 2011 →
   Deffayet–Woodard, JCAP 04 (2026) 081) is a published covariant carrier of {MOND statics + observed lensing +
   ΛCDM-grade expansion + claimed linear-order CMB/BAO/structure}, alive as of **two months ago**. Its gates are **open,
   not passed** (EFE/Cassini quadrupole uncomputed — with a fresh 2026 bound waiting; CMB claim reverse-engineered and
   unaudited; stability never settled beyond the quantum-effective-action stance). **TOE_TRILEMMA's perimeter sentence
   ("every published covariant host fails a gate") is owed an amendment: a fourth row whose status is "open gates," which
   is weaker than "closed perimeter."** That is a real retreat from the repo's strongest claim and is reported as such.
3. **For F4-as-modified-inertia specifically: OPEN, with the map sharpened.** The loophole class is modified *gravity* —
   it covariantizes the MOND **kernel**, not the **inertia**. No theorem forbids a covariant trajectory-nonlocal MI; no
   published realization exists; and two constraints derived/collected here pin what it must be: (i) the
   **conformal-collapse lemma** — any *pointwise* universal covariant m_eff is a conformal metric redefinition, i.e.
   modified gravity with zero extra lensing (dead on data); genuine covariant MI must carry Milgrom-1994's
   trajectory-nonlocality into the covariant setting; (ii) the **lensing-RAR wall** — metric-passive MI predicts
   baryon-only lensing, while the measured galaxy–galaxy lensing RAR has MOND amplitude; a covariant F4 therefore
   *cannot be the whole theory* — it needs a metric-side partner (which is what the DEW class supplies).

---

## §1 Milgrom's nonlocality theorem — what it forbids, what it permits

**Source:** Milgrom 1994, *Dynamics with a non-standard inertia-acceleration relation: an alternative to dark matter*,
Ann. Phys. 229, 384 — **arXiv:astro-ph/9303012**. Restated in Milgrom 2022 (**arXiv:2208.07073**, PRD 106, 064060) and
Famaey–Durakovic 2025 (**arXiv:2501.17006**, Encyclopedia of Astrophysics).

**Assumptions.** A single particle with kinetic action S_k[r(t); a0], a functional of the trajectory, with:
(i) Galilei invariance (rotations, translations, boosts; time translations);
(ii) Newtonian limit: a0 → 0 recovers the standard quadratic action;
(iii) MOND limit: a0 → ∞ with S_k ∝ 1/a0 (equivalently, deep-MOND space-time scale invariance — Milgrom 2022 phrases it
as (t,r) → λ(t,r) symmetry with G·a0 held fixed);
(iv) locality, defined as: L_k a function of finitely many time derivatives ("local or weakly nonlocal").

**The theorem (verbatim core, from the paper):** if the theory is Galilei invariant and local-or-weakly-nonlocal, then up
to a total derivative
> "L_k = ½αv² + L̃_k(a0, r⁽²⁾, r⁽³⁾, …)"

— boosts force the velocity to appear *only* in the standard quadratic term. The Newtonian limit requires **α = 1**; the
MOND limit (S ∝ 1/a0) requires **α = 0**. Contradiction. Hence:
> "Galilei-invariant theories for MOND, that are derivable from an action, **must be strongly non-local**."

**What exactly is forbidden.**
- Any *local* (finite-derivative) Galilei-invariant MI action with both limits. Corollary stated by Milgrom: the
  pointwise law μ(a/a0)·a = −∇Φ **"cannot be derived from an action"** — it can only be an effective/limiting relation.
  *Direct consequence for the repo: F4's pointwise μ_standard is necessarily the adiabatic limit of a nonlocal
  functional, never the action-level law itself. This was already the repo's standing caveat ("the full K(t−t′)
  construction remains open"); it is now anchored to the theorem.*
- The cautionary published instance: Costa, Franzmann & Pereira (**arXiv:1904.07321**) wrote a *local* higher-derivative
  MI Lagrangian — and pay the theorem's price in their own abstract: "higher derivative terms, leading to **exponentially
  unstable solutions** that must vanish," linear instabilities "valid for a characteristic timescale of at least 3 billion
  years," SEP violation, and Ostrogradsky instabilities only "tamed" piecewise. The local route confirms the theorem's
  bite; it does not evade it.

**What is explicitly PERMITTED.**
- **Strongly nonlocal worldline functionals.** Milgrom 1994 constructs explicit Galilei-invariant examples with both
  limits and calls the nonlocality "a blessing, as such theories need not suffer from the illnesses that are endemic to
  higher-derivative theories" (no worldline Ostrogradsky ghosts: the functional is not a finite-derivative truncation).
- **Exact algebraic circular-orbit relation:** for circular orbits in axisymmetric potentials, *any* MI theory yields
  μ(a/a0)·a = dΦ/dr with μ "simply related to the value of the kinetic action for a circular trajectory" (1994). So
  rotation-curve data (SPARC) pin **only the circular-orbit restriction** of the functional. F4's SPARC survival tests
  exactly this slice; eccentric/transient dynamics (Door IVa) probe the rest. Milgrom 2011 (**arXiv:1111.1611**) adds the
  second-tier freedom: MI EFE depends on the *history* of the external acceleration ("an EFE that depends on the
  accelerations all along its orbit"), and "it is even possible to construct MI theories with practically no EFE."
- **Concrete NR models now exist:** Milgrom 2022 (**arXiv:2208.07073**) builds time-nonlocal many-body MI models in
  Fourier form, ℐ[{r̂},ω,a0] = μ[𝒜(ω)/a0], reproducing rotation curves, the mass–asymptotic-speed relation, and a
  history-dependent EFE, with nonlocally-defined conserved P, E, L. On relativity, Milgrom's own expectation: "an
  eventual relativistic Fundamond will probably involve modification of **all parts of the action**" — i.e. matter AND
  gravity sectors (this dovetails with the lensing wall, §2). Field inventory as of 2025 (Famaey–Durakovic,
  **2501.17006**): "**No full-fledged theory of MOND as modified inertia exists**" — the trilemma's third cell verbatim.

**Bottom line §1:** the theorem forbids *locality*, not *covariantizability*. It positively licenses the worldline-
nonlocal class F4 belongs to — and simultaneously proves F4-as-written (a pointwise μ) cannot be fundamental.

---

## §2 Scope of the singular-surface wall, and the four carriers of T_eff

**The wall, correctly cited.** Two papers carry it:
- **arXiv:gr-qc/0607055** — Bruneton (solo), *On causality and superluminal behavior in classical field theories…
  k-essence and MOND-like theories*, PRD 75, 085013 (2007): Cauchy-problem/causality analysis of the k-essence class.
- **arXiv:0705.4043** — Bruneton & Esposito-Farèse, *Field-theoretical formulations of MOND-like gravity*, PRD 76,
  124012 (2007): the consistency review — MOND field theories are "unnaturally fine tuned," "unstable or inconsistent as
  field theories," and "do not remain always hyperbolic" within matter.
- Restated for the X-sign singular surface by **arXiv:2503.11174** (repo-banked 2026-06-06).

> **REPO HYGIENE (correction owed):** `REALIZATION_REDTEAM_galileon_singular_surface_2026-06-06.md` and
> `TOE_TRILEMMA.md` cite "Bruneton & Esposito-Farèse, gr-qc/0607055". That id is **Bruneton solo** (the
> causality/Cauchy paper); the BEF review is **0705.4043**. The kill is unchanged — both papers carry the case — but the
> author/id pairing should be repaired wherever it appears. (Minor second flag: the redteam doc's source list cites
> "Skordis & Złošnik AeST, 2304.05134"; **2304.05134** is Verwayen–Skordis–Bœhm (AeST quasistatic solutions); the
> original AeST paper is Skordis–Złośnik **2007.00082**, PRL 127, 161302.)

**What the wall actually is.** A statement about **local field theories with a propagating scalar** whose kinetic
function F(X), X = −½(∂φ)², must (for MOND) be non-analytic at X=0 and be visited on **both signs**: in-galaxy
quasi-static configurations have spacelike ∇φ (X of one sign); the cosmological branch has timelike φ̇ (the other). The
kinetic matrix then degenerates on an X=0 surface surrounding every bound object: the scalar stops propagating, the
Cauchy problem fails there, strong coupling diverges. The no-ghost/hyperbolicity conditions (f′>0, 2sf″+f′>0) cannot be
maintained across the straddle.

**Does it apply to F4? No — as stated, F4 has no carrier.** T_eff is a *worldline* quantity: the Deser–Levin/GEMS
temperature 2πT = √(a² + Λ/3) of a uniformly accelerated detector in dS (**arXiv:gr-qc/9706018**, CQG 14, L163 (1997)) —
covariantly meaningful per worldline, with no propagating field whose gradient must straddle signs. The wall constrains
one *choice of covariant carrier*, not the rule. The question is which field-theoretic object could carry T_eff. Four
candidates:

### (a) A k-essence scalar carrying T_eff — wall applies, verbatim
Encode T_eff (equivalently the local acceleration scale) in a scalar's gradient invariant — a "clock field" χ with
T_eff² ∝ kinetic invariants of χ. Then in-galaxy statics make ∂χ spacelike while the cosmological branch (which supplies
T_dS and hence a0) is timelike; MOND requires the non-analytic join; the BEF singular surface reappears around every
galaxy. **Closed — the banked kill transfers without modification.** (This is why "just promote T_eff to a field" is not
an escape.)

### (b) The local Rindler/causal-horizon temperature itself (Jacobson-style) — breaks on the frame problem
Jacobson (**arXiv:gr-qc/9504004**) derives the EFE from δQ = T dS on local Rindler horizons — no new propagating field;
the "carrier" is the horizon structure of each local boost frame. Two things break when MOND is loaded on:
1. **The frame problem (the sharp one).** The Unruh/Deser–Levin temperature is *observer-dependent*. A star orbiting in
   a galaxy is in free fall: its proper acceleration is **exactly zero**, so its GEMS temperature is T_dS regardless of
   the galaxy, and m_eff ∝ dT_eff/da evaluates at a=0 — **no MOND for geodesic matter** (worse: F4's μ(0)=0 would
   destroy inertia for all free-fall, planets included). The "a" in F4 is the *Newtonian-frame* acceleration — the
   proper acceleration of the static/orbit-supporting frame, not of the star. Covariantly, that is first-derivative
   metric information (connection coefficients), which the equivalence principle gauges to zero at a point: **no local
   covariant scalar of the metric alone encodes g_N.** So the carrier must be either an extra frame field (→ route c) or
   a nonlocal composite of the metric (→ route d / the DEW trick). Milgrom saw this in 1999 (**astro-ph/9805346**): "For
   the vacuum to serve as substratum for inertia a body must be able to read in it its non-inertial motion" — the vacuum
   *is* the frame, and reading it is intrinsically nonlocal. (That paper is also the repo's F1: T(a)−T(0) with
   T ∝ √(a²+a0²), a0=√(Λ/3) — the difference form the repo killed ×54,000 on ephemerides.)
2. **The published instance fails in detail.** Verlinde's emergent gravity (**arXiv:1611.02269**) — apparent dark force
   from dS entanglement entropy at a0 ~ cH0 — is derived only for static, spherically symmetric, isolated configurations,
   with no covariant field equations; tested against the RAR it requires depressed M/L and predicts radius-dependent
   residuals that are not observed (Lelli–McGaugh–Schombert, **arXiv:1702.04355**, MNRAS 468, L68).
**Status: open in principle, no working MOND realization, and it inherits the frame problem the moment "acceleration"
enters the entropy functional.**

### (c) A vector/aether — solves the frame problem by fiat, reinstates the Cassini bill (now larger)
A unit-timelike A^μ supplies the frame that (b) lacks; this is AeST (Skordis–Złośnik **2007.00082**; quasistatic
phenomenology Verwayen–Skordis–Bœhm **2304.05134**): CMB ✓, c_GW = c ✓, ghost-free ✓ — and the repo-banked Cassini
quadrupole kill. **New since the banking:** Park, Hees, Famaey, Desmond & Durakovic, **arXiv:2602.17884** (Feb 2026,
DE440 ephemerides): **Q2 = (1.6 ± 1.8)×10⁻²⁷ s⁻²** (1σ; 40% better than Hees et al. 2014, **arXiv:1402.6950**, which had
(3±3)×10⁻²⁷), with claimed **3–15σ** tension against external-galaxy rotation-curve fits for "modified gravity versions
of the MOND paradigm," a ≤2% (95%) cap on the MOND boost at the Sun's galactocentric radius, and the explicit statement
that the solar system now out-constrains wide binaries for classical modified-gravity MOND. The aether route's bill went
up. Note the class language — **modified inertia evades this bound by class** (trajectory-dependent EFE; the repo's F4
Saturn check passed ×4 on the tail effect), which the field's own 2025 review now leans on: "Most likely, these
constraints … imply that modified gravity MOND needs a new scale in addition to acceleration … **or that MOND rather
results from a more radical modification of inertia**" (Famaey–Durakovic, **2501.17006**, as retrieved, ellipses theirs).

### (d) Worldline-nonlocal couplings to the metric only — the F4-native route; one sub-case dies, one stays open
**(d1) Pointwise m_eff is a conformal collapse (lemma, elementary, derived here).** Let the particle mass depend on ANY
scalar I[g](x) evaluated along the worldline — including nonlocally-built ones:
S = −∫ m(I[g](x)) √(−g_μν dx^μ dx^ν) = −∫ √(−[m² g_μν] dx^μ dx^ν). Matter universally sees g̃ = m²(I[g])·g — a
**conformal metric redefinition**, i.e. modified *gravity* in disguise. Null geodesics are conformally invariant, so
photons are undeflected beyond GR-of-baryons: **zero extra lensing**. This is exactly the classic conformal no-lensing
disease that killed RAQUAL-era scalar-tensor MOND and forced TeVeS's disformal term (reviewed in **0705.4043**), and the
core of the Soussa–Woodard argument (**astro-ph/0307358**). Two conclusions: (i) pointwise covariant "modified inertia"
is not modified inertia at all — and it is data-dead; (ii) by Milgrom-94, pointwise-in-time is "local" and was never
genuine MI anyway. **Genuine covariant MI must be trajectory-nonlocal: a retarded kernel K(τ,τ′) over the worldline's
history, not a mass function of position.**
**(d2) The genuine trajectory-nonlocal worldline functional — OPEN, no theorem, no realization, ingredients in print.**
What it needs, and where each piece already exists:
- a covariant cosmic frame **without a propagating aether**: DEW build u^μ[g] as the normalized gradient of a nonlocal
  scalar (χ = −□⁻¹1 in **1405.0393**; a past-lightcone-volume construction in **1106.4984**) — no independent Cauchy
  data, no Cassini-billed vector;
- a covariant "Newtonian acceleration" along the worldline: DEW's invariants ∂_μ[□⁻¹(R_αβu^αu^β)] reduce to ∇Ψ in
  statics — □⁻¹ *lowers* the derivative count, which is precisely how the EEP obstruction (first derivatives are gauge)
  is evaded — the published existence proof that the activation variable F4 needs CAN be built covariantly;
- the temperature: Deser–Levin per worldline (**gr-qc/9706018**);
- the NR template to lift: Milgrom 2022's ℐ[{r̂},ω] models (**2208.07073**).
No one has assembled these. The obstruction is engineering + the §2-wall below, not a theorem.

### The lensing-RAR wall (new, data-side, full weight — found while auditing, reported both ways)
Metric-passive MI (inertia modified; EFE and metric standard, sourced by baryons) ⇒ photons are deflected by the
baryons-only metric ⇒ the *lensing* RAR should track g_bar with **no phantom**. The measured galaxy–galaxy lensing RAR
(Brouwer et al. 2021, KiDS-1000 — the dataset the repo's LR program is currently re-deriving) follows the MOND-amplitude
ν down to ~10⁻¹³ m s⁻². Pending the repo's LR-1 replication, **pure modified inertia under-predicts weak lensing by the
full phantom factor at lensing radii.** Consequences: a covariant F4 must either MONDify the metric photons see (i.e.
acquire a modified-gravity partner sector — which is what DEW engineer via their a = k·r·b′ potential tie, and what
AeST's vector does), or fail lensing. This does NOT touch F4 as a *dynamics* phenomenology (SPARC, Saturn, WB — all
massive-matter tests), and it is consistent with Milgrom-2022's own expectation that a relativistic version modifies
"all parts of the action." But it closes the door on "covariant modified inertia *alone*" as the missing object. The
trilemma's missing object is therefore more precisely: **a covariant theory whose matter sector carries
trajectory-nonlocal MI and whose metric sector carries the lensing.**

---

## §3 The DEW loophole — the nonlocal-metric program, audited end to end

**The chronology (every step pinned):**

| Year | Paper | What happened |
|---|---|---|
| 2003 | Soussa–Woodard, **astro-ph/0307358** (PLB 578, 253) | No-go: any *stable* purely-metric MOND becomes conformal in the weak field ⇒ cannot produce the observed lensing. Frames the whole program; they already flag "a formulation with a very weak instability" as the way out. |
| 2011 | Deffayet–Esposito-Farèse–Woodard, **arXiv:1106.4984** (PRD 84, 124054), *Nonlocal metric formulations of MOND with sufficient lensing* | The loophole opens. Nonlocal scalars X[g], Y[g] built from ∂□⁻¹(R_αβu^αu^β ± R/2) with u^μ a nonlocal composite; □⁻¹ lowers derivative count so an acceleration-scale invariant exists covariantly. The two potentials are tied (a = k·r·b′) so the model gives the MOND force **and** observed lensing — SW evaded by intrinsic weak-field non-analyticity (the MOND regime is never linearizable). Solar system: corrections suppressed at a ≫ a0 by the interpolation structure. Stability: "our model has a cubic Lagrangian in the weak fields and will therefore suffer the same potential instabilities as any such theory" (their words). Causality: retarded □⁻¹ by partial-integration "trick"; honest derivation deferred to Schwinger–Keldysh. Status: phenomenological quantum effective action; clusters still need extra mass. |
| 2014 | DEW, **arXiv:1405.0393** (PRD 90, 064038) | Full field equations; FRW specialization; u^μ = −g^μν∂_νχ/√(…), χ = −□⁻¹1. Localization with auxiliary scalars: unconstrained, "two scalar ghosts"; with retarded/constrained initial data the auxiliaries carry **no independent modes** — "eliminates the ghosts (and in fact all the modes associated with the scalars)". **Two a0 cases: constant, and a0 → α[g] ≡ D_μu^μ/6π ∝ H(t)** — the latter called "more phenomenologically interesting" (avoids ~10³² tuning of the free function's argument across cosmic history). |
| 2016 | Kim, Rahat, Sayeb, Tan, Woodard, Xu, **arXiv:1608.07858** (PRD 94, 104009) | Free function numerically reconstructed to reproduce the ΛCDM expansion from BBN through vacuum domination. Unavoidable deviation at z < 0.088: **H0 comes out ~4.5% high vs ΛCDM** — they note this may *resolve* the Hubble tension (a falsifiable, direction-correct surprise, not a pathology). |
| 2018 | Tan–Woodard, **arXiv:1804.01669** (JCAP 1805, 037) | **The recorded failure that stalled the program:** linearized perturbations about the ΛCDM history show "the MOND enhancement is **not sufficient to allow ordinary matter to drive structure formation**" (sub-horizon). Fixes discussed, not implemented. 2018–2024: the MOND side sits broken. |
| 2020 | Pardo–Spergel, **arXiv:2007.00555** (PRL 125, 211101) | The external challenge: any no-DM gravity needs a growth Green function with sign-changing ~150 Mpc features to erase baryon oscillations — effectively a demand for sharp scale-dependence/nonlocality. |
| 2024 | Deffayet–Woodard, **arXiv:2402.11716** (JCAP 05 (2024) 042), *The Price of Abandoning Dark Matter Is Nonlocality* | The answer to Pardo–Spergel, and the thesis of this door in a title. Emergent dust: T_μν = ρ[g] ∂_μφ[g] ∂_νφ[g] with u_μ = ∂_μφ, (∂φ)² = −1 (mimetic-adjacent — cf. repo-banked 2503.11174) reproduces "perturbations in the cosmic microwave background, baryon acoustic oscillations and structure formation" without DM. |
| 2025/26 | Deffayet–Woodard, **arXiv:2512.10513** (JCAP 04 (2026) 081) | **The program is alive.** A single model interpolating cosmology ↔ bound systems via Z[g] ≡ (4c⁴/a0²) g^μν ∂_μ[□⁻¹R_αβu^αu^β] ∂_ν[□⁻¹R_ρσu^ρu^σ] → |∇Ψ|²-like in statics. **The regimes are distinguished by the SIGN of Z** (cosmology Z<0; deep MOND 0<Z≲1; Newtonian Z≫1), with f(Z) = ½Z·exp(−√|Z|/3) shutting the MOND sector off on the cosmological branch. a0 is a fixed constant in this version (the 2014 α[g] ∝ H variant remains available in the class); the emergent-dust density is set by ρ0 = 45a0²/16πG. |

**The structural inversion (the key fact for Door II).** The timelike/spacelike sign-straddle that is *fatal* for a
local scalar (BEF: kinetic degeneracy on the X=0 surface) is the *design feature* of the nonlocal model: Z[g] crosses
zero harmlessly because **nothing propagates with a kinetic matrix built from f′(Z)** — the auxiliaries carry no Cauchy
data (retarded prescription), so the would-be degeneracy surface is not a characteristic surface of any degree of
freedom. The Maggiore-school systematization of nonlocal quantum-effective-action gravity (Belgacem–Dirian–Foffa–
Maggiore, **arXiv:1712.07066**) supplies the general conceptual frame (nonlocal QEA; retarded kernels causal; auxiliary
fields not new dof). This is the precise sense in which the singular-surface wall does **not** generalize beyond local
field carriers.

**Open gates of the loophole class (named, honest — "open" ≠ "passed"):**
1. **EFE/Cassini Q2 — the live kill-test.** Not computed anywhere in the program; the 2026 paper lists "how distant
   masses affect the nonlocal functional Z[g](x)" as future work. Meanwhile **2602.17884** sets Q2 = (1.6±1.8)×10⁻²⁷ s⁻²
   with 3–15σ class-level tension for modified-gravity MOND. DEW-class is modified gravity with geodesic matter — the
   generic expectation is an AQUAL-like quadrupole. Caveat both ways: the free function is unconstrained enough that an
   exponentially-screened branch might survive; whether an RAR-compatible μ and a Q2-safe EFE *coexist in this class* is
   exactly the bounded calculation this door should commission (§4).
2. **CMB: claimed, unaudited.** The 2024 result is reverse-engineered at linear order by a single group; no independent
   Boltzmann-code confrontation, no public implementation. (Famaey–Durakovic 2025 does not even discuss the class — the
   field has not yet audited it.)
3. **Stability: acknowledged since 2011, never settled.** The weak-field cubic instability concern stands; the QEA
   stance is the defense, not a theorem.
4. **No derivation.** "We do not believe fundamental theory is nonlocal" (DEW-II); the inflationary-graviton resummation
   is a conjecture. The loophole class is, epistemically, a **Bohr-rung object like F4 itself**: selected/engineered, not
   derived.
5. **GW sector unexamined** for the MOND models (cousin nonlocal-DE models predict modified GW luminosity distance —
   a future discriminator; c_GW itself is plausibly c, but uncomputed here).

**Could F4 live inside it?** Two answers, both honest:
- **As modified inertia: no.** DEW-class matter is geodesic; the MOND is in the field equations. F4's second-tier MI
  content — trajectory-dependent EFE, the MI two-body relation, Q2-evasion *by class* — is not realized. The two
  candidates are in fact **Cassini-anticorrelated**: if Park+26's class tension holds against DEW's EFE, the loophole
  dies by the same sword as AeST while MI-proper survives it; if DEW's EFE turns out screened, the loophole leads.
- **As the kernel: yes.** The free function is unconstrained by the construction (DEW-I fix only the deep-MOND
  coefficient and the lensing tie), and Z → (4c⁴/a0²)|∇Ψ|² in statics means f(Z) can encode ν matching
  μ_standard = x/√(1+x²). The *selection story* (m_eff ∝ dT_eff/da; Deser–Levin susceptibility) does not transfer —
  nothing in DEW is a temperature. And per the repo's branch discipline: the class's dynamical-a0 variant is
  **a0 ∝ H(t) (rising toward high z) — the rival branch**, not the framework's declining √ρ_DE; at z=0 they are
  degenerate, at z ≳ 1 they diverge. DEW shows the class can carry an *evolving* a0 at all (the structurally relevant
  point); it does not support either branch.

---

## §4 Verdict, kill-tests, and the bounded calculation

**THEOREM? No.** The audited chain: Milgrom-94 kills locality (and licenses nonlocality, NR-proved); the EEP/local-
flatness argument kills *local metric* carriers of an acceleration scale (no local covariant scalar = g_N) — evaded in
print since 2011 by □⁻¹ composites; Soussa–Woodard kills stable-conformal purely-metric MOND — evaded by DEW's engineered
second potential and intrinsic non-analyticity; the BEF singular surface kills local k-essence carriers — inverted into
the regime switch of the 2026 nonlocal model. **Every link has a published evasion; no obstruction theorem can be
assembled from these parts.** An obstruction-theorem closure of the law rung is therefore NOT available — and equally,
none of the banked kills is weakened: they all stand, each confined to its local-field-theory scope.

**LOOPHOLE? Yes — the nonlocal pure-metric class (DEW 2011 → DW JCAP 2026), with open gates.** It is the closest
published thing to "covariant MOND without the trilemma's kills": no propagating scalar (no BEF wall), no aether (no
postulated frame), lensing by construction, ΛCDM-grade background, claimed linear cosmology, alive as of April 2026.
It is **modified gravity, not modified inertia** — it covariantizes the kernel, not the clock. Its named kill-tests:
the EFE quadrupole vs Q2 = (1.6±1.8)×10⁻²⁷ s⁻² (2602.17884); an independent CMB/Boltzmann audit of 2402.11716; a
stability statement beyond the QEA stance; GW friction.

**For F4: OPEN — with the search space collapsed further.** What this door adds to the repo's map:
1. **Pointwise covariant MI is impossible-as-MI and dead-on-data** (conformal-collapse lemma + no-lensing): any honest
   covariant F4 is a *trajectory-nonlocal* worldline functional — Milgrom-94's nonlocality survives covariantization
   intact and gets stronger.
2. **The frame must be supplied**, and the only published Cassini-safe way is DEW's nonlocal composite u^μ[g] (an
   aether's job without an aether's bill).
3. **The lensing-RAR wall**: covariant MI alone under-predicts lensing by the phantom factor; the missing object is a
   **hybrid** — trajectory-nonlocal MI in the matter sector + a metric sector that carries the lensing (DEW-class being
   the only published candidate partner). This matches Milgrom-2022's "modification of all parts of the action."
4. The trilemma perimeter sentence must be amended (fourth row: DEW-class, status OPEN GATES — weaker than "closed").

**The bounded calculation that settles the live fork (pre-registerable):**
> **Compute the solar-system EFE quadrupole Q2 of the 2512.10513 model** — the Galaxy's field entering Z[g] at the Sun
> (quasistatic; external g_ext ≈ 1.8×10⁻¹⁰ m/s²; one free function, pinned to the RAR by the repo's own SPARC machinery)
> — and compare to Q2 = (1.6 ± 1.8)×10⁻²⁷ s⁻² (2602.17884), scanning the free-function family for whether RAR-fit and
> Q2-safety coexist.
> - **Q2 ≳ 10⁻²⁶ robustly** ⇒ the loophole class joins AeST at the Cassini wall ⇒ the trilemma perimeter RE-CLOSES, and
>   modified inertia (Q2-evading by class) is again the only open cell — now precisely specified as the hybrid of (3).
> - **Q2 ≲ 10⁻²⁷ achievable with an RAR-compatible μ** ⇒ the loophole is the leading covariant host; the repo should
>   confront its kernel with it directly (encode μ_standard in f(Z); re-run the 2016-style background fit; test the
>   H0 +4.5% signature against 2026 data).
Secondary bounded items: (a) quantify the metric-passive-MI lensing deficit against the repo's LR-1 ESD profiles (same
battery, one new model column — cheap, and it makes wall (3) quantitative); (b) the d2 existence check: does ANY
retarded worldline kernel K(τ−τ′) built from {g, u^μ[g], T_eff} reproduce ν in the adiabatic limit while destabilizing
geodesics only below a0 — now a well-posed construction problem (Door II residue).

**Scope note (flagged, not resolved here):** the trilemma table covers AeST, single-scalar hosts, and MI; **BIMOND**
(Milgrom's bimetric MOND, arXiv:0912.0790) is a published covariant host not in the table (its CMB story is undeveloped
and its GW/Cassini gates un-audited in the repo). The amended table should either add it or state its exclusion reason.

---

## Citations (arXiv ids, role)

| id | role |
|---|---|
| astro-ph/9303012 | Milgrom 1994, Ann. Phys. 229, 384 — the nonlocality theorem (α=1 vs α=0); circular-orbit exactness; permits nonlocal functionals |
| astro-ph/9805346 | Milgrom 1999 — inertia from vacuum; T ∝ √(a²+a0²), a0=√(Λ/3); the frame-from-vacuum statement (= repo's F1 source) |
| 1111.1611 | Milgrom 2011 — MI second-tier predictions; history-dependent EFE; "practically no EFE" possible |
| 2208.07073 | Milgrom 2022, PRD 106, 064060 — explicit NR time-nonlocal MI models; "relativistic Fundamond … all parts of the action" |
| 1904.07321 | Costa–Franzmann–Pereira — local MI Lagrangian; pays Ostrogradsky (confirms the theorem's bite) |
| gr-qc/0607055 | Bruneton (solo), PRD 75, 085013 — causality/Cauchy of k-essence & MOND-like theories [repo citation repair] |
| 0705.4043 | Bruneton–Esposito-Farèse, PRD 76, 124012 — the consistency review (fine-tuning; hyperbolicity loss; conformal no-lensing lineage) |
| 2503.11174 | mimetic-MOND restatement of the singular surface (repo-banked) |
| gr-qc/9504004 | Jacobson 1995 — EFE as equation of state (route-b basis) |
| gr-qc/9706018 | Deser–Levin 1997, CQG 14, L163 — GEMS temperature 2πT = √(a²+Λ/3) (F4's T_eff, covariant per worldline) |
| 1611.02269 | Verlinde 2016 — emergent dark force at a0~cH0; static/spherical only (route-b instance) |
| 1702.04355 | Lelli–McGaugh–Schombert 2017, MNRAS 468, L68 — Verlinde vs RAR: fails in detail |
| 2007.00082 | Skordis–Złośnik, PRL 127, 161302 — AeST (route c) |
| 2304.05134 | Verwayen–Skordis–Bœhm — AeST quasistatic solutions [repo citation repair] |
| 1402.6950 | Hees–Folkner–Jacobson–Park 2014, PRD 89, 102002 — Cassini Q2 = (3±3)×10⁻²⁷ s⁻² |
| 2602.17884 | Park–Hees–Famaey–Desmond–Durakovic 2026 — Q2 = (1.6±1.8)×10⁻²⁷ s⁻²; 3–15σ vs modified-gravity MOND; MI evades by class |
| astro-ph/0307358 | Soussa–Woodard 2004, PLB 578, 253 — stable purely-metric MOND ⇒ conformal ⇒ no lensing |
| 1106.4984 | DEW 2011, PRD 84, 124054 — nonlocal metric MOND with sufficient lensing (the loophole opens) |
| 1405.0393 | DEW 2014, PRD 90, 064038 — full field equations; u^μ[g]; ghost removal by constrained auxiliaries; a0 ∝ H variant |
| 1608.07858 | Kim et al. 2016, PRD 94, 104009 — ΛCDM expansion reconstructed; H0 +4.5% at z<0.088 |
| 1804.01669 | Tan–Woodard 2018, JCAP 1805, 037 — structure formation FAILS in the 2014 model (the stall) |
| 2007.00555 | Pardo–Spergel 2020, PRL 125, 211101 — the price-of-no-DM challenge (Green-function features) |
| 2402.11716 | Deffayet–Woodard 2024, JCAP 05, 042 — "The Price of Abandoning Dark Matter Is Nonlocality"; CMB+BAO+growth mimicry |
| 2512.10513 | Deffayet–Woodard 2026, JCAP 04 (2026) 081 — the interpolating model; sign-of-Z switch; EFE listed as open |
| 1712.07066 | Belgacem–Dirian–Foffa–Maggiore — nonlocal QEA gravity: conceptual status (causality, no new dof) |
| 1112.3960 | Famaey–McGaugh 2012 Living Review — field-standard MI inventory (context) |
| 2501.17006 | Famaey–Durakovic 2025 Encyclopedia chapter — "no full-fledged MI theory exists"; "Cassini ⇒ … more radical modification of inertia" |
| 0912.0790 | Milgrom — BIMOND (scope-note: missing trilemma row) |
