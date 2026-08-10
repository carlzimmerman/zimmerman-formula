# The Completion

**A relativistic field theory carrying a₀ = κc√(Gρ_Λ)**

Zimmerman, Carl P. — Briar Creek Tech
Assembled 2026-08-09; **v2 same day; v3 same day**. Every numbered property below is backed by a committed, runnable
script that exits non-zero on failure. Scripts named at each line.
**v2 changes:** row 13's shift-charge cluster route is **withdrawn** (killed by the 1-Mpc
confrontation: smooth accretion restores ξ→1 for any cold IC) and replaced by the **a₀-bump
environment response**, which passed a five-environment matrix AND its perturbation health check;
the health check carved two hard constraints (Λ_D ≤ 8.4×10⁻⁷; amplitude ≤ 2.7× fiducial). The
coefficient row now reads as **measured**: κ = 0.551 ± 0.043, ±0.063 if the H₀ tension is carried as a
systematic (κ ∝ a₀/H₀).
**v3 changes:** (i) the **full AeST perturbation matrix** for the bump term is now DONE and added as
row 17 — c_T = 1 exact, no-ghost as a theorem, quasi-static closure derived, amplitude cap softened
to a band; non-claim 2c is updated accordingly. (ii) **Non-claim 2 is corrected**: v2's "by item 13
it is absent where rotation curves are measured" was a dangling pointer — row 13 was withdrawn *in
the same version* — so the galaxy-interior status of the Q-sector dust is **REOPENED** and now
stated as its own open problem (non-claim 2d). v2 carried this internal inconsistency for several
hours; the correction runs against the framework's interest and is flagged rather than hidden.
(iii) §3's amplitude cap now states its units (4.5 Mpc⁻² = 2.7× the fiducial 1.65 Mpc⁻²).

---

## 1. The action

$$
S = \int d^4x\,\sqrt{-g}\;\Big[\;\underbrace{\frac{R - 2\Lambda_{\rm bare}}{16\pi G}}_{\text{Einstein–Hilbert}}
\;+\;\underbrace{\mathcal{L}_{\rm aether}[A^\mu,g]}_{\text{unit-timelike }A^\mu A_\mu=-1}
\;+\;\underbrace{\mathcal{F}(Y,Q)}_{\text{the dark sector}}\;\Big]\;+\;S_{\rm matter}[g,\psi]
$$

with the two scalar invariants built from the khronon φ and the aether A^μ,

$$
Q \equiv A^\mu \nabla_\mu \varphi,
\qquad
Y \equiv \big(g^{\mu\nu} + A^\mu A^\nu\big)\nabla_\mu\varphi\,\nabla_\nu\varphi .
$$

This is **Aether-Scalar-Tensor** (Skordis & Złośnik 2021, PRL **127** 161302) — chosen because it is
the only relativistic MOND-class theory that reproduces the CMB. The framework's content is entirely
in the choice of the free function 𝓕, which **factorises**:

$$
\boxed{\;\mathcal{F}(Y,Q) \;=\; \underbrace{\frac{a_0^2}{8\pi G}\,\mathcal{F}_Y\!\left(\frac{Y}{a_0^2}\right)}_{\text{MOND}}
\;+\;\underbrace{K(Q)}_{\text{dark energy + dark matter}}\;+\;\underbrace{A\,B\!\left(\tfrac{Y}{a_0^2}\right)(Q-Q_0)^2}_{a_0\text{-bump response (v2)}}\;}
$$

$$B(y)=\frac{y}{(1+y)^2}$$

The third term (v2) is a **position-dependent Helmholtz mass** $\mu^2_{\rm eff}=A\,B(g^2/a_0^2)$
**peaked at the framework's own $a_0$** — the location costs nothing ($Y/a_0^2$ is already the
Y-sector's normalisation); one new calibrated amplitude $A\approx1.7$ Mpc$^{-2}$. *The dark sector's
response is resonant at the MOND transition, and clusters are the cosmic objects that live at $a_0$*
($R_{500}$ at $0.33$–$0.58\,a_0$).

### 1.1 The Y-sector — MOND

𝓕_Y is fixed by the framework's Route A kernel ν(y) = 1/(1 − e^(−√y)), y = g_bar/a₀. In AQUAL
variables it is the closed parametric pair

$$
\mu(u) = 1 - e^{-u}, \qquad x(u) = \frac{u^2}{\mu(u)}, \qquad u = \sqrt{y},\; x = g_{\rm obs}/a_0 .
$$

with the normalisation

$$
a_0 \;=\; \kappa\,c\sqrt{G\rho_\Lambda} \;=\; \frac{cH_\Lambda}{Z} \;=\; c^2\sqrt{\frac{\Lambda}{32\pi}}
\;=\; 9.3619\times10^{-11}\ {\rm m\,s^{-2}},
\qquad \kappa=\tfrac12,\;\; Z = 2\sqrt{8\pi/3}.
$$

**κ = ½ is FITTED, not derived.** See §4.

### 1.2 The Q-sector — an offset DBI khronon

$$
\boxed{\;K(Q) \;=\; -M^4 \;+\; \mu^2\Lambda_D^2\left[\,1 - \sqrt{1 - \frac{u^2}{\Lambda_D^2}}\,\right],
\qquad u \equiv Q - Q_0,\quad |u| < \Lambda_D \;}
$$

Three jobs from one function:

| piece | limit | what it is |
|---|---|---|
| the **offset** −M⁴ | u = 0, K′ = 0 | ρ = −K = M⁴, p = K = −M⁴ ⟹ **w = −1 exactly**: dark energy |
| the **deviations** | u ≪ Λ_D | K → μ²u²/2 ⟹ w → 0: **dust**, i.e. the dark matter |
| the **saturation** | u → Λ_D | K bounded, K′ → ∞ ⟹ w → 0 again: kills the early stiff phase |

Parameters: **M** (vacuum scale, M⁴ = ρ_Λ), **μ** (Helmholtz mass), **Λ_D** (DBI field-space scale),
**I₀** (the conserved shift charge = the dust amount).

---

## 2. What is verified

| # | property | value / statement | script |
|---|---|---|---|
| 1 | **Lensing** — the test that killed modified inertia | Φ = Ψ ⟹ γ_PPN = 1, M_dyn/M_lens = 1 exactly. **21.2σ → 0.601σ** | `mi_relativistic_completion_aest_2026.py` |
| 2 | **Kernel embeds** in 𝓕_Y | deep-MOND μ→x exact; Newtonian μ→1; x(u) a bijection (h′ = e^(−u)(1+u) > 0); free function **convex** | same |
| 3 | **Newtonian residual** | e^(−√y) = 3.6×10⁻³⁴⁵⁷ at Earth's orbit | same |
| 4 | **Dark energy is not an input** | w = −1 **exactly** at the condensate minimum — proved, not assumed | `mi_condensate_vacuum_energy_a0_2026.py` |
| 5 | **Ghost-free** over the whole field range | K″ = μ²(1−s²)^(−3/2) > 0 for all \|s\|<1 | `mi_dbi_khronon_2026.py` |
| 6 | **Subluminal** everywhere | c_s² = Λ_D s(1−s²)/(1+Λ_D s) ≤ 0.385 Λ_D | same |
| 7 | **The published no-go is dissolved** | Blanchet & Skordis 2024 §4.3.1's 455× conflict **reverses sign**: bounded pressure ⟹ w→0 early ⟹ cosmology becomes a *lower* bound on μ⁻¹, same direction as MOND | same |
| 8 | **Theorem**: why no polynomial works | for K ~ uⁿ, early-time w → 1/(n−1). Quadratic 1, quartic ⅓, sextic ⅕ — all fail. **Only boundedness gives w→0** | same |
| 9 | **CMB acoustic peaks** — real CLASS run | at Λ_D ≤ 10⁻², c_s²(recomb) = 2.9×10⁻⁸; TT unchanged to **0.069%**, P(k=0.2) to 1.71%. Indistinguishable from CDM | `mi_dbi_cmb_class_run_2026.py` |
| 10 | **BTFR** | exact, from convexity | `mi_route_a_field_theory_2026.py` |
| 11 | **g⁻² Lorentz violation** | **restored** by the aether (pure Bekenstein–Milgrom had lost it) | `mi_relativistic_completion_aest_2026.py` |
| 12 | **a₀ tied to Λ** | a₀ = m_cond/(4√π) with m_cond = M²/(√2 M_Pl), M⁴ = ρ_Λ — agrees to **0.076%** | `mi_condensate_vacuum_energy_a0_2026.py` |
| 13 | **Clusters** (v2) | ~~shift-charge IC route~~ **withdrawn**: killed by the 1-Mpc confrontation — cluster R500 and galaxy-outskirt lensing share a scale with disjoint requirements, correlated Gaussian ICs cannot select environments, and **smooth accretion restores ξ→1 for any cold IC**. Replaced by the **a₀-bump response** (row 15) | `mi_ic_route_1mpc_confrontation_2026.py` (9/9) |
| 14 | **Directional EFE signal** | pure MI predicted *exactly zero*; AQUAL-class predicts 1–4% signed; first firing gave Â = +2.95, p = 0.029, **with the AQUAL sign** | `mi_dr4_anisotropy_and_gated_2026.py` |
| 15 | **a₀-bump environment response** | passes all five environments: cluster (calibration, μ²_eff = 0.23 Mpc⁻²), galaxy interior 0.034% of M_b (RAR cost 4×10⁻⁴ dex), galaxy 1 Mpc 1.2% vs the 5.9% strict bound, linear cosmos 0.6% of mean matter, solar 10⁻¹⁹. Vanishes on FRW (Y=0) and is second-order in perturbations ⇒ linear CMB/P(k) untouched by construction. Evades both prior kills (a response has no charge to advect; couples to environment directly) | `mi_a0_bump_response_2026.py` (10/10) |
| 16 | **…and its health check** | **no ghosts ever** (kinetic contribution 2AB ≥ 0, = 0 on FRW), no Ostrogradsky sector; FRW gradient health **excludes the old Λ_D = 10⁻² and forces Λ_D ≤ 8.4×10⁻⁷** (window stays 3.7 orders); halo gradient health **caps A ≤ 2.7× fiducial, excluding the demanding end of Mistele's cluster band** — a two-sided falsifiable pinch; free signature: cluster anisotropic stress at O(0.6) | `mi_a0_bump_health_2026.py` (11/11) |
| 17 | **…and the FULL perturbation matrix (v3)** | with all aether mixings: **c_T = 1 exact** (the new terms are algebraic in the metric — GW170817 safe by construction); **no-ghost is a THEOREM** (the bump's kinetic addition is rank-1 PSD in the χχ entry ⟹ Weyl monotonicity: it cannot lower any eigenvalue of AeST's healthy kinetic matrix; closed-form 2×2 + 200 random 4×4); unit-norm gives δA⁰ = −ΦA⁰ ⟹ δQ = χ̇ − Q₀Φ — the quasi-static phenomenology of row 15 is **derived, not assumed**; gradient block exact: ΔG = 2λ[[q, 2y^{3/2}B″],[2y^{3/2}B″, yq]], q = (3y²−8y+1)/(1+y)⁴; integrating out the aether softens the amplitude cap: at base_a = 1 the band is **A_max ∈ [2.72, 4.46]× fiducial = [4.49, 7.36] Mpc⁻²** (**v4 correction:** the earlier "(2.7–7.4)× fiducial" spliced fiducial units with Mpc⁻², making the band look 1.66× wider at the top than it is — `base_a_lookup_and_robustness_2026.py`, 12/12). **The base_a lookup is now DONE and it converts the caveat rather than closing it:** base_a is built from AeST's single aether constant K_B, which has *never been measured* — every value in print is a fiducial (0.1 dominant; the PRL's own 0.3 model is captioned MOND-incompatible), the only quantitative bound is the paper's own stability window 0 < K_B < 2, and GW170817 constrains it not at all (in Einstein-aether language K_B = c₁ = −c₃ with c₂ = c₄ = 0, so the tensor-speed combination c₁+c₃ vanishes identically for every K_B — consistent with this row's independent c_T = 1 result). The quasi-static *phenomenology* is K_B-blind — G̃ = (1−K_B/2)Ĝ absorbs it, turning SZ2021 Eq. (6) into Bekenstein–Milgrom, and K_B appears **zero times** in the dedicated quasi-static paper (arXiv:2304.05134, 1.4 MB verified) while surviving in the cosmological equations (their Eq. 11) — but the mixing ratio is an internal matrix entry taken *before* that diagonalisation, so which combination it equals (2−K_B, K_B, or 1) is **a short derivation still owed, not a lookup**. Robustness computed over all three: **Mistele's 34× end is excluded under every candidate** (margins 9.4×, 1.7×, 7.6×; only base_a ≤ 0.056 could admit it), while **the 4× edge flips** — excluded at base_a = 1.9, marginal at 0.1 and 1; FRW bound Λ_D ≤ 8.4×10⁻⁷ survives (Φ-mixing Poisson-suppressed, 3×10⁻⁴); **open flags**: λ-suppressed tachyon-type vector mass for y > 1 interiors (WATCH); SZ2021's known k < μ unboundedness sits at the Hubble scale (within 15%) at μ⁻¹ = 4392 Mpc — relocated, not resolved | `mi_aest_full_matrix_bump_2026.py` (11/11) |

---

## 3. Parameter count, honestly

| | ΛCDM | this completion |
|---|---|---|
| dark sector | Ω_c, Ω_Λ | M (= ρ_Λ^{1/4}), I₀, μ, Λ_D, **A (v2)** |
| MOND scale | — | a₀ — **not independent**, = m_cond/(4√π) via item 12 |
| bounds | — | Λ_D: 1.9×10⁻¹⁰ ≪ Λ_D ≤ 8.4×10⁻⁷ (**health-bounded, v2**; 3.7 orders); A ≈ 1.7 Mpc⁻² calibrated on clusters, **health cap A ≤ 4.5 Mpc⁻² = 2.7× fiducial** (row 16; the full matrix widens it to [2.72, 4.46]× fiducial = [4.49, 7.36] Mpc⁻² at base_a = 1 — row 17, where the base_a fork and its robustness are stated); μ⁻¹ = 4392 Mpc (item 12); I₀ ≈ Ω_dm (an IC) |

So: **five dark-sector numbers against ΛCDM's two** (v2 adds A), with a₀ derived from one of them rather than
added. Not fewer parameters. What it buys is that Λ, dark matter and MOND come from **one function**
instead of three unrelated sectors.

---

## 4. What is NOT claimed — read this before quoting anything above

1. **κ = ½ IS NOT DERIVED.** Item 12 looks like a derivation and is not. `a₀ = m_cond/(4√π)` is
   *algebraically identical* to `a₀ = ½√(Gρ_Λ)` and to `Z = 2√(8π/3)` — three costumes, one
   statement — and the residue is **convention-dependent** (4√π with the reduced Planck mass, √2 with
   the non-reduced). A derived number cannot depend on a bookkeeping choice. It is a **relabelling**,
   as this corpus's own theorem already established. What genuinely moved: "why κ = ½?" becomes "why
   is a₀ = m_cond/(4√π)?", which is sharper because m_cond is a *derived* quantity of a real field
   theory rather than a definition.
2. **Dark matter EXISTS**, at the full Ω_dm. Removing the pressureless component moves H₃/H₁ by 54%
   and no refit absorbs it (Δχ² > 400). What does **not** exist is a dark-matter *particle*: it is the
   Q-sector of the same scalar that supplies Λ and MOND. **(v3 correction:** v2 continued "and by
   item 13 it is absent where rotation curves are measured" — a dangling pointer, since v2 itself
   withdrew row 13. See 2d. **The defensible slogan shrinks to "no dark-matter particle" — never
   "no dark matter", and "none in galaxies" is now an open problem, not a result.)**
2d. **(v3) WHERE THE DUST SETTLES IS THE SHARPEST OPEN PROBLEM.** The 1-Mpc confrontation's own
   smooth-accretion theorem (row 13's killer) implies the Q-sector dust falls into *every* collapsing
   basin, galaxies included. Two branches are then live: **(favorable)** the settled condensate
   relaxes to the Helmholtz-preferred profile — ρ_c tracking the potential, flat, centrally
   evacuated (`mi_virialisation_verdict_2026.py`: ξ ∝ R², galaxy-interior cost ~6×10⁻⁵ dex) — and
   galaxies are safe by orders of magnitude; **(fatal)** the dust retains CDM-like central
   concentration and the completion overshoots its own best data by the banked 2.06–4.42×. Which
   branch obtains is a **nonlinear dynamics question — relaxation of the condensate toward the
   static profile within a Hubble time — that no group has ever computed for AeST.** It is scheduled
   as this program's next calculation (N-body-class, staged from spherical symmetry up). Until it is
   done, galaxy-interior cleanliness is an *assumption the theory needs*, not a result it owns.
   **(Same-day postscripts, stages 1 AND 2.** Stage 1 (`nbody_2026/stage1_condensate_relaxation_
   2026.py`, 11/11) found a sound-crossing bound Λ_D ≳ 1.2×10⁻⁹. **Stage 2
   (`nbody_2026/stage2_spherical_collapse_2026.py`, 10/10) WITHDRAWS stage 1's favorable branch —
   crossing ability is necessary, not sufficient — and finds the fatal branch is the DEFAULT at
   every Λ_D in the health window, within the fluid description:** the bounded DBI pressure cannot
   support galactic dust (even the optimal c_s² = 0.385Λ_D at the ceiling falls 1.38× short of the
   halo virial parameter), the Helmholtz profile's capacity at μ⁻¹ = 4392 Mpc is ~10⁻⁷ of the
   captured charge, and the basin's dust free-falls to a sub-kpc caustic within a Hubble time —
   overshooting the 10-kpc RAR point by ~0.72 dex. **Stage 2b
   (`nbody_2026/stage2b_base_a_attribution_and_A_conflict_2026.py`, 15/15) then corrected TWO of
   stage 2's own claims, in opposite directions.** (i) *A hope withdrawn:* stage 2 said base_a
   could move the FRW ceiling and so carried "mortal weight" for the galaxy problem — **false**;
   the ceiling is √(CLASS_DMG·μ²/(2A·L₀²·pk)), in which base_a does not appear, and its only
   possible channel was already bounded at 3.2×10⁻⁴ by row 17's F1. base_a's real and only load is
   the **cluster** pinch (the Mistele 34× end stays excluded for any base_a ∈ [0.5, 4]; the 4× edge
   is marginal for base_a ≲ 1). (ii) *A deficit withdrawn:* stage 2's "supported ⇒ possibly
   survivable" was **right**, and stage 2b's attempt to tighten it rested on a circular estimator
   (caught by its own negative control); the honest figure is 0.052 dex at 1 Mpc, inside the ~0.1
   dex outskirt tolerance. **What replaces the lost door is tighter than it was:** the ceiling
   scales as A^(−1/2), so galactic dust support needs A ≤ 0.87 Mpc⁻² while clusters calibrate
   A = 1.65 and Ref. Mistele's modelling wants 6.6–56 — **one parameter, two jobs, opposite
   directions; the bump's success on clusters monotonically deepens its galaxy failure.** And a
   **new falsification on existing data**: support is v_c-dependent, splitting at
   v_c = c√(0.385 Λ_D,max) = 170 km/s — below it the interior is clean, above it spirals sit 0.72
   dex off the RAR — so the fluid branch predicts a break inside the SPARC range that **is not
   observed**. Remaining door: stage 3 (wave/field dynamics at the caustic, outside the fluid
   description), which must keep interiors clean at v_c > 170 km/s *without lowering A*. 2d remains
   OPEN; its fluid-description branch is now falsified rather than merely disfavoured.)**
2b. **The coefficient is MEASURED, not derived: κ = 0.551 ± 0.043** (distance-free SPARC estimator),
   and **± 0.063 if the H₀ tension is carried as a systematic**, since κ ∝ a₀/H₀ at full strength.
   ½, 1/√3, √(3/8) and 0.40 all sit inside 2σ. (v2 correction: v1's ±0.043 omitted the ρ_Λ term.)
2c. **The a₀-bump response is a CANDIDATE, not a result**: it has passed the environment matrix,
   its isolated-term health check, and (v3) the **full AeST perturbation matrix with aether mixings
   (row 17)**. Still owed: a **real cluster-model fit** (the amplitude is calibrated on a single
   summary number — nobody, this program included, has fit real cluster mass profiles), the
   **base_a identification** — the *lookup* is done (row 17: K_B is a never-measured free
   parameter bounded to 0 < K_B < 2), but which K_B-combination the mixing entry equals is a short
   derivation still owed; it decides only the 4× edge, the 34× exclusion being robust — and a
   dedicated vector-sector analysis.
   The health-vs-Mistele amplitude pinch could still kill it.
3. **The post-recombination growth history is NOT verified.** Item 9 covers the acoustic peaks only.
   Holding c_s² at its peak value for all time *destroys* P(k=0.2), so the pass depends essentially on
   the bump being transient (it peaks at z ≈ 189). **A patched CLASS fluid carrying c_s²(a) is
   required, not optional.**
4. **(v4 rewording — the original referred to withdrawn row 13.)** The dust component's
   small-scale initial conditions are **not confronted with Lyman-α.** The withdrawn IC route
   needed a khronon transfer function T ≈ 0.33 at k ≈ 4.5 Mpc⁻¹ (ΛCDM-excluded); the surviving
   picture (standard cold dust + the bump response) should be Ly-α-safe by construction, but that
   is **asserted, not computed — the confrontation remains owed
   item in the programme.**
5. **Cassini Q₂ is inherited** (3–15σ) and is not relieved by anything here.
6. **PPN preferred-frame parameters** α₁, α₂ for this 𝓕 have not been computed against lunar-laser and
   binary-pulsar bounds.
7. **The wide-binary target is the point-field asymptote only.** γ_v = √ν(y_extN); the full
   nonlinear AQUAL-EFE solve is owed.
8. **This is not a theory of everything** and no part of it addresses the Standard Model. The
   2026-06-23 retraction stands.

---

## 5. The falsifiable predictions

| prediction | value | how to test |
|---|---|---|
| wide-binary boost | γ_v = √ν(y_extN) | **Gaia DR4**, pre-registered and hash-stamped |
| directional EFE asymmetry | 1–4%, signed | already firing at p = 0.029 with the right sign |
| cluster-to-cluster **scatter** in the residual | σ(ξ)/ξ ≈ 0.02–0.60 | existing cluster samples — **(v4) separates the a₀-bump response (scatter tracks each cluster's distance from the resonance, rows 15–17) from any fixed-scale mechanism, which predicts uniformity** (the two prior candidates are withdrawn) |
| cluster mass **profile** misfit | ρ_c flat, M_c ~ r³, can go negative | fit clusters with the khronon profile instead of NFW |
| g⁻² Lorentz violation | computable s_μν | SME sector bounds |
| accelerated structure formation | earlier massive objects | JWST high-z massive galaxies (McGaugh et al. 2024) |

---

## 6. Credit

ν = √(1+1/y) is **Milgrom 1999 PLA 253:273 eq 9**. MOND: Milgrom 1983 ApJ 270:365. AQUAL:
Bekenstein & Milgrom 1984 ApJ 286:7. TeVeS: Bekenstein 2004 PRD 70:083509. **AeST: Skordis & Złośnik
2021 PRL 127:161302** — the completion itself. Ghost condensate: Arkani-Hamed, Cheng, Luty &
Mukohyama 2004 JHEP 0405:074; nonlinear: +Wiseman 2007 JHEP 0701:036. K(Q) = μ²(Q−1)² and the ghost-
condensate identification: Verwayen, Skordis & Złośnik 2024; **Blanchet & Skordis 2024 JCAP
11(2024)040** — including §4.3.1, the no-go this work dissolves. Quasi-static AeST: Durakovic &
Skordis 2024 JCAP 04:040; Verwayen, Skordis & Boehm 2024 MNRAS 531:272. **Mistele, McGaugh &
Hossenfelder 2023 A&A 676:A100** — the weak-lensing bounds that killed this program's first two
cluster mechanisms and now two-sidedly bound the third (rows 15–17). GDM bound: Kopp,
Skordis, Thomas & Ilić 2018 PRL 120:221102. Ly-α floor: Rogers & Peiris 2021 PRL 126:071302. RAR
scatter: Desmond 2023. Accelerated structure formation: McGaugh, Schombert, Lelli & Franck 2024.

**The distinctive content of this work is the coefficient — a₀ = κc√(Gρ_Λ) with κ = ½ — its
embedding in 𝓕_Y, the offset-DBI Q-sector, and items 7, 8, 9, 12 and 13. Everything else is cited
above and is not mine.**
