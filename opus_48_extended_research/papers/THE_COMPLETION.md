# The Completion

**A relativistic field theory carrying a₀ = κc√(Gρ_Λ)**

Zimmerman, Carl P. — Briar Creek Tech
Assembled 2026-08-09; **v2, v3, v4, v5 same day; v6 2026-08-10**.
**v6 changes — an ERRATUM against v5, filed against my own argument.** v5's non-claim 2d rested one of
its three steps on a **category error**: it bounded the *export* of the dust's energy from a galaxy by
the khronon's own polytropic sound speed (≈690 Gyr). ∇_μT^μν = 0 bounds the **total energy**, not the
**flux velocity**; the bound on how fast energy can leave a region is **causality**, and AeST has two
massless tensor modes at exactly *c* — by this paper's own row 17. An O(*c*) export channel therefore
exists in the theory as written (1 Mpc in 3.3 Myr). **That step is withdrawn.** Also withdrawn: the
claim that the leak rates "lock" at ρ_Λ/ρ_dust = 2.60 — that is merely today's density ratio.
**The conclusion survives on stronger, published, transport-independent grounds:** exporting the
energy removes it from the *galaxy*, not the *universe*, so the measured global budget decides —
a halo-gated conversion needs a converted fraction ζ ≈ 0.6 against the **epoch-marginalised** bound
ζ < 0.0204 (Planck) to 0.0374 (+lensing+BAO+SN+DES) [McCarthy & Hill, PRD **108**, 063501], over by
16–29×, and would leave Ω_dr,0 ≈ 0.196 ≈ 2100× today's radiation density; the dust→dark-energy channel
needs far more than the published |δ₀| ≤ 6.7×10⁻⁴. And the halo gate is **adverse**, not protective:
dilution goes as a_c, so later injection leaves *more* residue. **The lensing theorem (ρ+3p vs ρ+p) is
untouched and is what carries the result.** Banked as a genuine asset: the Y-gate's FRW exactness makes
recombination-era N_eff immunity *exact*. Also recorded, against expectation: the **background** does
not require dark matter at all (Kunz's dark degeneracy, confirmed numerically — a single free w_X(z)
reproduces ΛCDM's H(z) with baryons alone); the binding constraint is **CMB lensing**, which forces the
clustering to survive to z < 0.30. Every numbered property below is backed by a committed, runnable
script that exits non-zero on failure. Scripts named at each line.
**v5 changes — the largest revision, and it runs against the programme's interest.** A six-stage
sequence (`nbody_2026/`, every stage committed and green) settles the galaxy-interior question that
v3 reopened as non-claim 2d, and **settles it adversely: the Q-sector cannot also be absent from
galaxies, and the repair space of local, energy-preserving modifications is provably empty.** Three
results carry it: (i) *the dust mass IS the conserved shift charge* (ρ = Q₀n with ρ/n = Q₀ regardless
of any added Y-dependent Q-mass), so it cannot be suppressed locally — which retro-explains three
withdrawn mechanisms; (ii) *unlocking the charge does not unlock the energy* (∇_μT^μν = 0 holds
regardless — though v6 withdraws the transport step that accompanied this, see the v6 banner);
(iii) **⭐ dynamics responds to ρ + 3p but
lensing responds to ρ + p, and no equation of state kills both** — so the same no-slip identity that
underwrites row 1 forbids hiding the dust. Also corrected here: v3/v4's claim that the DBI cap bounds
the dust *density* (it bounds the pressure; ρ_exc is linear in u and diverges at saturation), and
v4's spliced amplitude band. **Rows 1–12 and 15–17 are untouched.**
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
| the **deviations** | u ≪ Λ_D | K → μ²u²/2 is the **pressure**, while ρ_exc = Q₀μ²u is **linear** in u ⟹ w = u/2Q₀ → 0: **dust**, i.e. the dark matter. *(v5: the linearity is why the dust mass equals the conserved charge — see non-claim 2d.)* |
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
| 17 | **…and the FULL perturbation matrix (v3)** | with all aether mixings: **c_T = 1 exact** (the new terms are algebraic in the metric — GW170817 safe by construction); **no-ghost is a THEOREM** (the bump's kinetic addition is rank-1 PSD in the χχ entry ⟹ Weyl monotonicity: it cannot lower any eigenvalue of AeST's healthy kinetic matrix; closed-form 2×2 + 200 random 4×4); unit-norm gives δA⁰ = −ΦA⁰ ⟹ δQ = χ̇ − Q₀Φ — the quasi-static phenomenology of row 15 is **derived, not assumed**; gradient block exact: ΔG = 2λ[[q, 2y^{3/2}B″],[2y^{3/2}B″, yq]], q = (3y²−8y+1)/(1+y)⁴; integrating out the aether softens the amplitude cap: at base_a = 1 the band is **A_max ∈ [2.72, 4.46]× fiducial = [4.49, 7.36] Mpc⁻²** (**v4 correction:** the earlier "(2.7–7.4)× fiducial" spliced fiducial units with Mpc⁻², making the band look 1.66× wider at the top than it is — `base_a_lookup_and_robustness_2026.py`, 12/12). **The base_a lookup is now DONE and it converts the caveat rather than closing it:** base_a is built from AeST's single aether constant K_B, which has *never been measured* — every value in print is a fiducial (0.1 dominant; the PRL's own 0.3 model is captioned MOND-incompatible), the only quantitative bound is the paper's own stability window 0 < K_B < 2, and GW170817 constrains it not at all (in Einstein-aether language K_B = c₁ = −c₃ with c₂ = c₄ = 0, so the tensor-speed combination c₁+c₃ vanishes identically for every K_B — consistent with this row's independent c_T = 1 result). The quasi-static *phenomenology* is K_B-blind — G̃ = (1−K_B/2)Ĝ absorbs it, turning SZ2021 Eq. (6) into Bekenstein–Milgrom, and K_B appears **zero times** in the dedicated quasi-static paper (arXiv:2304.05134, 1.4 MB verified) while surviving in the cosmological equations (their Eq. 11) — but the mixing ratio is an internal matrix entry taken *before* that diagonalisation, so which combination it equals (2−K_B, K_B, or 1) is **a short derivation still owed, not a lookup**. Two further primary-source facts sharpen this: **there is no SZ supplemental material at all** (verified against the published LaTeX source — the deferral named a document that does not exist), and **the PRL's own quasi-static limit sets Aⁱ = 0 by ansatz**, so under the parent paper's own treatment there is no aether mode to integrate out and the mixing vanishes (the follow-ups, which let Aⁱ = ∂ⁱα live, are the setting in which the mixing term exists at all). Robustness computed over all four candidates: **Mistele's 34× end is excluded under every one** (margins 9.4×, 1.7×, 7.6×, 12.5×; only base_a ≤ 0.056 could admit it), while **the 4× edge flips** — excluded under 2−K_B *and* under the PRL's own no-mode ansatz, marginal under K_B and 1, so the marginality this paper asserts is the *less* well-supported half of the fork; FRW bound Λ_D ≤ 8.4×10⁻⁷ survives (Φ-mixing Poisson-suppressed, 3×10⁻⁴); **open flags**: λ-suppressed tachyon-type vector mass for y > 1 interiors (WATCH); SZ2021's known k < μ unboundedness sits at the Hubble scale (within 15%) at μ⁻¹ = 4392 Mpc — relocated, not resolved | `mi_aest_full_matrix_bump_2026.py` (11/11) |

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
   "no dark matter"; and (v5) **"none in galaxies" is WITHDRAWN as a claim of this theory**, not
   merely open — see 2d.)**
2d. **(v5) THE Q-SECTOR CANNOT ALSO BE ABSENT FROM GALAXIES — FALSIFIED WITHIN THE THEORY AS
   WRITTEN, AND THE REPAIR SPACE IS NOW PROVABLY EMPTY.** This is the largest change since v1 and it
   runs against the programme's interest. v2 asserted "none in galaxies" via a pointer to withdrawn
   row 13; a six-stage sequence (`nbody_2026/`, all scripts committed, 20/20 + 15/15 + 12/12 + 15/15
   + 15/15 + 11/11) then settled the question the pointer had concealed.

   **The physics.** The 1-Mpc smooth-accretion theorem implies the Q-sector dust falls into *every*
   collapsing basin, galaxies included. What happens next was the open problem, and it closed in
   four steps:
   - **Nothing stops the collapse.** Wave (k⁴ ghost-condensate) pressure gives a soliton scale of
     **0.18 AU** at halo density — eight orders below the RAR region — and it *shrinks* as ρ grows
     (λ ∝ ρ^−¼); a 1 kpc wave core would need M below the Lyman-α fuzzy-DM floor. The dust *is* an
     n = 1 polytrope (p = Kρ², c_s² = 2Kρ rising) with a genuine **mass-independent 105 pc**
     equilibrium — but that lies **14.4× past DBI saturation**, where c_s → 0 and the stiffening
     switches off. Endpoint: a black hole of the captured share, **falsified 5.8×10⁵× against
     Sgr A\*** (4.3×10⁶ M☉ from individual stellar orbits — no mass model, kernel or cosmology in
     the comparison). *(v5 corrects v3/v4 here: an earlier draft claimed the DBI cap bounds the
     density and yields a ~250 pc core. μ²u²/2 is the **pressure**; exactly, ρ_exc = Q₀μ²u is
     **linear** in u and diverges at saturation. Withdrawn.)*
   - **THEOREM: the dust mass IS the conserved shift charge.** ρ = Q₀·n with n the shift-charge
     density, and **ρ/n = Q₀ independently of any Y-dependent Q-mass, of any shape or amplitude.**
     So no such term can change how much dust a galaxy carries — *a conserved charge cannot be
     suppressed locally, only moved (gravity moves it inward) or not conserved.* This single
     statement retro-explains three withdrawn mechanisms: the shift-charge IC route, the Φⁿ
     response, and an acceleration-gated suppressor built and killed in stage 4–5 (its eight gates
     all tested the field amplitude u; the observable is n, and at fixed charge the suppressor makes
     a region a *cheaper* place to store charge — it attracts what it was built to expel).
   - **Breaking the shift symmetry gets furthest, and fails.** A *global* potential is incompatible
     as an identity (dV/dt = V′φ̇ must vanish for w = −1, while the condensate needs φ̇ = Q₀ ≠ 0);
     quantitatively the leak rates lock at Γ_n/Γ_V = ρ_Λ/ρ_dust = 2.60, so clearing a galaxy in
     1 Gyr drifts ρ_Λ by 47× and protecting ρ_Λ forces a 180 Gyr charge lifetime. A **Y-gated**
     breaking, 𝓕 ⊃ −W(Y/a₀²)V(φ) with W(0) = 0, *defeats* that — on FRW the symmetry is **exact**,
     so cosmology is untouched identically. But **unlocking the charge does not unlock the energy**:
     ∇_μT^μν = 0 holds regardless. **(v6 erratum:** v5 added that the energy therefore *cannot leave*,
     bounding its export by the khronon's polytropic sound speed at ≈690 Gyr. That was a category
     error — a conservation law bounds total energy, not flux velocity; the causal limit is *c*, and
     row 17's tensor modes travel at exactly *c*. **Withdrawn.** What kills the export route instead is
     the *measured global budget*: a halo-gated conversion needs ζ ≈ 0.6 against the epoch-marginalised
     ζ < 0.0204–0.0374 [McCarthy & Hill, PRD **108**, 063501] — over by 16–29× — leaving Ω_dr,0 ≈ 0.196,
     some 2100× today's radiation density; and dust→Λ needs far more than |δ₀| ≤ 6.7×10⁻⁴. The gate is
     adverse rather than protective, since dilution goes as a_c.**)
   - **⭐ AND LENSING CLOSES IT BY A THEOREM.** Transforming the equation of state almost works: the
     dynamical source ρ + 3p vanishes at exactly **f = 1/3**, and the field-strength gate makes that
     a *stable fixed point* rather than a tuning. But **dynamics responds to ρ + 3p while lensing
     responds to ρ + p** — at f = 1/3 the lensing source is still (2/3)ρ, giving M_lens/M_dyn ≈ 29
     against an observed 1.0–1.3. Generally, ρ + 3p = 0 requires w = −1/3 and ρ + p = 0 requires
     w = −1: **incompatible. No equation of state renders a given energy density invisible to both
     orbits and light; the only such configuration is ρ = 0**, which the transport bound forbids
     reaching. *The no-slip identity Φ = Ψ that makes this theory's modified-gravity arm work — the
     property that killed its modified-inertia arm at 21σ and underwrites item 1 — is the same
     property that forbids hiding the dust.*

   **Status, stated without spin.** The galaxy-interior problem is not a missing mechanism: it is a
   conservation law (energy, via general covariance), plus a transport bound, plus lensing. **The
   repair space of local, energy-preserving modifications is provably empty.** The defensible slogan
   is therefore **"no dark-matter particle"** and nothing more; **"none in galaxies" is withdrawn as
   a claim of this theory.** What remains open is a structural change — the Q-sector not acquiring
   the galactic energy in the first place — against which the smooth-accretion theorem stands for
   any cold initial condition. Items 1–12 and 15–17 are untouched by all of this.

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
