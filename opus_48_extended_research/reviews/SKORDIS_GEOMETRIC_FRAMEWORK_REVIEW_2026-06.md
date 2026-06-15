# Route 1 — Skordis body-of-work review: the geometric machinery, what the framework can borrow, and at what cost

*Opus 4.8 extended research, 2026-06-15. Both-ways. Primary sources read in full (PDF text-extracted, not
abstract-only): Skordis-Złośnik 2021 PRL 127 161302 = arXiv:2007.00082; Durakovic-Skordis 2024 JCAP 04 040 =
arXiv:2312.00889; Mistele-McGaugh-Lelli-Schombert-Li 2023 arXiv:2301.03499. Cross-checked against the banked
`aest_radial_aether_eom.py` (which already carries Eq.5 verbatim), `cmb_third_peak_dm_mimic.py`, and
`OPEN_PROBLEM_yphi32_KQ.md`. Quarantine respected throughout: a0/Z never asserted derived.*

---

## 1. The AeST action (the geometric core) — verbatim from arXiv:2007.00082 Eq.5

S = ∫d⁴x √(−g)/(16π G̃) [ R − (K_B/2) F_μν F^μν + 2(2−K_B) J^μ ∇_μφ − (2−K_B) Y − F(Y,Q) − λ(A_μA^μ+1) ] + S_m[g]

- Field content: ONE metric g_μν, a **unit-timelike vector** A_μ (A·A=−1, enforced by λ), a **scalar** φ.
- F_μν = 2∇_[μ A_ν]; J_μ = A^α∇_α A_μ (the aether "acceleration"); Q = A^μ∇_μφ; Y = q^μν∇_μφ∇_νφ with
  q^μν = g^μν + A^μA^ν (the projector ORTHOGONAL to A). Shift-symmetric in φ.
- This IS a geometric (Lorentz-violating) completion: matter couples ONLY to g (so EEP holds), but the aether
  picks out a preferred frame, exactly the structure Carl's de Sitter-Unruh inertia needs (the cosmic rest frame
  A_μ with ∇·A = 3H on FRW — verified in the banked `clean_slate_field_theory.py`).

## 2. Where a0 enters — and where it does NOT (the load-bearing decoupling)

**a0 lives in the SPATIAL-gradient sector Y.** The nonrelativistic template (Eq.2) has the scalar EOM
∇·[(dJ/dY)∇φ]=4πĜρ with the MOND limit FORCED to:

  J → [ 2λ_s / (3(1+λ_s) a0) ] Y^{3/2}   as ∇φ→0   — "It is in this limit that a0 appears" (verbatim).

So a0 enters via a **Y^{3/2}** term, exactly the non-analytic 3/2 power Carl's framework carries (`𝒴^{3/2}`), with
the deep-MOND √-law. The parameter λ_s controls Newton↔MOND tracking/screening; G_N = (1+1/λ_s)Ĝ.

**On FRW, Y = 0 identically** (q⁰⁰=0 because A aligns with the timelike direction): "a0 does not appear in the
linear cosmological regime but will play a role once nonlinear terms from F(Y,Q) kick in" (verbatim). This is the
structural CMB-safety Carl's `OPEN_PROBLEM_yphi32_KQ.md` item 2 already banked — and it is the SAME fact that
makes the unification fail at the CMB (next section).

## 3. The cosmological sector K(Q) — the dark-matter-mimic, and the unification cost

On FRW, K(Q̄) ≡ −½F(0,Q̄), Q̄ = φ̄̇/N. Skordis-Złośnik propose (Eq.4):

  K = −2Λ + K₂(Q̄−Q₀)² + …   — Λ the CC, K₂ and Q₀ free parameters.

This is **shift-symmetric k-essence with a minimum at Q₀≠0**, which (Arkani-Hamed et al ghost-condensate result
they cite, ref [87-89]) gives **dust (ρ̄∝a⁻³) + cosmological constant** — i.e. a CDM-LIKE component AND dark energy
from one scalar. They call it the "(gravitational) Higgs phase." THIS is the genuine machinery: the scalar's
energy density acts pressureless at early times and drives the CMB peaks / the matter power spectrum.

**The cost, in the paper's own words (the smoking gun for the unification claim):**
- The CDM-mimic density: 8πG̃ρ̄ = Q dK/dQ − K; integrating the φ̄ EOM gives dK/dQ = **I₀/a³** for initial condition
  I₀, so ρ̄ = ρ̄₀/a³ with **8πG̃ρ̄₀ = Q₀ I₀**. Then verbatim: **"As the solution depends on the initial condition
  I₀, the density ρ̄ is not (classically) predicted."**
- The CC: **"The CC in this model remains a freely specifiable parameter, just as in the ΛCDM model"** (verbatim).

I VERIFIED numerically (`a0` decoupling, script in this session): scaling a0 by ×0.1/×1/×10 leaves the required
Q₀I₀ to hit Planck's Ω_cdm h²=0.12 **unchanged** — 8πG̃ρ̄₀ = Q₀I₀ contains NO a0 and NO Λ. The MOND scale a0 (in
the Y-sector) and the DM-mimic density (the integration constant I₀ in the Q-sector) are **independent slots of the
same free function F(Y,Q)**. (My a0 = c²√(Λ/32π) reproduces 9.354e-11, consistent.)

**=> THE UNIFICATION COST IS EXACT AND FROM THE HORSE'S MOUTH.** AeST fits the CMB (their Fig.1: ΛCDM-quality TT/EE
with Cosh/Exp K(Q) functions, residuals within the data) and the SDSS DR7 MPS (Fig.2). But the early-universe
dark-matter density is set by I₀ (an integration constant) + K₂,Q₀,Z₀ (free function parameters), NOT by a0↔Λ.
Carl's distinctive claim — "two dark sectors, ONE number" — is true in galaxies (a0↔Λ via Y^{3/2}) but **breaks at
the CMB**: you need a SECOND, independently-tuned number (~Ω_cdm at recombination). The CMB is not fishy; AeST FITS
it; the honest verdict is the unification-COST, not a data artifact.

## 4. The lineage (the geometric structure that fixes lensing) — credit where due

- **TeVeS (Bekenstein-Sanders, refs [53,54]):** introduced the unit-timelike vector to turn a conformal into a
  **disformal** relation, so that the two metric potentials are equal (Ψ=Φ) and DM-mimicking solutions ALSO bend
  light correctly. TeVeS was bimetric and was KILLED by GW170817 (c_T≠c). AeST keeps the {φ, A_μ} content but uses
  ONE metric + a B_μ-class non-canonical kinetic term engineered so **c_T = c in all backgrounds** (req. v). This
  is the verified "no gravitational slip" property: A⁰∼√(−g⁰⁰) ⇒ Ψ=Φ ⇒ lensing mass = dynamical mass. The
  framework's banked "AeST has no slip" is CORRECT and is the structural reason the lensing front reduced 4/6 args.
- **Einstein-Aether (Jacobson-Mattingly):** the generalized-Einstein-Aether / khronon vector machinery is the
  parent of A_μ; the banked `aest_radial_aether_eom.py` and the khronon PPN corner (agentU) descend from it.

## 5. The cluster mass term (Durakovic-Skordis 2024, arXiv:2312.00889) — better than the banked summary, still squeezed

The quasistatic limit of AeST adds, beyond AQUAL, a **mass term µ²Φ** with µ = √(2K₂/(2−K_B)) Q₀ — i.e. µ is set
by the SAME K₂,Q₀ that set the cosmological dust density. Below r_C ∼ (r_M µ⁻²)^{1/3} you get MOND; beyond r_C, Φ
**oscillates**. They require µ⁻¹ ≳ 1 Mpc so galaxies stay MONDian.

Reading the FULL paper (not the abstract): the cluster result is **more favorable than the banked "wrong-signed"
verdict, and I correct that, both ways:**
- Right-signed enhancement DOES exist: "the gas profiles in AeST were found to be more compressed than both the
  Newtonian case and MOND, signifying a **stronger gravitational force than in MOND, or equivalently, more apparent
  dark matter**" (verbatim). The RAR shows a **peak ABOVE MOND** at an acceleration set by µ, the mass, and the
  potential's boundary value.
- The "negative mass" is the TAIL, not the whole story: "The peak ... is **followed by** a deficit ... interpreted
  as a negative phantom mass" at LOWER accelerations (the outskirts). The observed cluster RAR (Chae, Eckert et al)
  ALSO shows peak-then-deficit — so the SHAPE qualitatively matches.
- BUT it is explicitly NOT a demonstrated cure: "AeST possesses the **qualitative features** to address the problem
  of galaxy clusters in MOND ... **it remains to be seen whether this effect can be corroborated with real data** ...
  A quantitative analysis ... is **left for future work**" (verbatim). No fit to eRASS1 η(R500), no magnitude match.

**The squeeze (Mistele 2023, arXiv:2301.03499, full HTML read):** galaxy-galaxy weak lensing stays MOND-like out to
a_b ≳ 10⁻¹³ m/s² (≈1 Mpc), which requires **m²/f_G < 1 Mpc⁻²** (and < 0.001 Mpc⁻² if MONDian to 10⁻¹⁵). But the
**cluster** boost requires **m²/f_G ≳ 1 Mpc⁻²**. The SAME mass parameter is pulled in OPPOSITE directions — this is
the banked "squeezed by galaxy weak-lensing." So: the cluster candidate is framework-INTRINSIC and right-signed in
its peak, but (a) unquantified vs the eRASS1 η, (b) µ is a FREE parameter (not from a0/Λ — it is the K₂,Q₀ pair),
and (c) the weak-lensing bound and the cluster need can't be simultaneously satisfied with one µ on current evidence.

## 6. What the framework can BORROW vs what stays free/tuned (both ways)

GENUINELY AVAILABLE from Skordis's geometry:
- The field content is FORCED by Carl's own premises (metric from geometry; unit-timelike A_μ from the dS-Unruh
  cosmic rest frame; scalar φ from a long-range low-a force) — `clean_slate_field_theory.py` already shows this.
- The **Y^{3/2} power is forced** (√-law ⇒ n=3/2; AND independently by Singh 2026's SO(4,1) conformal symmetry).
- CMB-safety of a0 is **structural** (q⁰⁰=0 ⇒ Y=0 on FRW), not tuned.
- No-slip lensing is **structural** (A⁰∼√−g⁰⁰ ⇒ Ψ=Φ).
- A covariant, ghost-free, c_T=c host that FITS the CMB+MPS exists — this is real and is the machinery that makes
  the DM-illusion thesis viable at all.

STILL FREE / TUNED (the honest ledger — these are NOT derived from a0=c²√(Λ/32π)):
- The **coefficient Z** (a0 = cH_Λ/Z, Z≈5.79): `OPEN_PROBLEM_yphi32_KQ.md` is a RIGOROUS NULL across six
  horizon-entropy routes; Singh 2026 himself writes a0=c²/(ξℓ_dS) with ξ "O(1) fixed by matching," not derived.
  AeST gives no route to Z either — the Y^{3/2} prefactor 2λ_s/(3(1+λ_s)a0) carries a0 as INPUT.
- The **cosmological function K(Q)** shape (Cosh/Exp/Higgs) and its parameters K₂, Q₀, Z₀ — chosen to fit, not
  derived. This is `OPEN_PROBLEM` item C, still open.
- The **DM-mimic density I₀** — an integration constant, "not classically predicted" (their words).
- The **CC Λ** — "freely specifiable, just as in ΛCDM" (their words). [The framework's distinctive content is that
  the SAME Λ also sets a0; AeST does not enforce that link — it is an EXTRA posit Carl adds on top of AeST.]
- The cluster mass µ — free (the K₂,Q₀ pair), and double-bound by lensing-vs-clusters.

## 7. Is the geometry a route to DERIVE Z or the scalar density? — NO (rigorously), but it CONSTRAINS the form

There is a geometric CORE (aether vector + dS structure + Y^{3/2}) that ties a0 to Λ at the level of FORM and SCALE
(a0 ∼ √Λ is forced by the Gibbons-Hawking horizon). But neither AeST nor any of the six banked horizon-entropy
routes FORCES the coefficient: every route reduces to a0 = κ·c√(Gρ_Λ) with κ un-pinned (κ=½⇒Z=5.79, Verlinde
⇒Z=6, thermal⇒Z=2π). And AeST's K(Q)/I₀ machinery means the cosmological dark-matter density is a SEPARATE free
input, so the geometry does NOT collapse "two dark sectors" to one number at the CMB. **Form + scale: yes.
Coefficient + CMB unification: no — still posited.**

---

## Bottom line (locked, both ways)
Skordis's AeST is the real, covariant, ghost-free, c_T=c, no-slip geometric host for Carl's DM-illusion thesis: it
delivers MOND in galaxies via a forced Y^{3/2} term carrying a0, fits Planck CMB + SDSS MPS, fixes lensing, and
offers a framework-intrinsic, RIGHT-SIGNED (peak-above-MOND) cluster candidate. The HONEST costs: (1) the CMB fit
needs a SECOND number — the integration constant I₀ / the K₂,Q₀,Z₀ free function — so "two dark sectors, one
number" FAILS at the CMB (the unification is galactic-only); (2) the cluster cure is qualitative, unquantified vs
eRASS1, and the mass µ is squeezed between the weak-lensing bound (m²/f_G<1 Mpc⁻²) and the cluster need
(≳1 Mpc⁻²); (3) Z and K(Q) remain posited/tuned, not derived. NOT fishy — AeST is the most honest thing in the
literature here; the losses SOFTEN (cluster shape matches; CMB is fit, not falsified) but do not erase, and the
unification claim pays a real, nameable price.
