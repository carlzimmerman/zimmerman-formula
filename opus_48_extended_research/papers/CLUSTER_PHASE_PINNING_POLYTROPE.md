# The Aether–Scalar–Tensor Dark Sector Is a γ = 2 Polytrope: the Cluster Helmholtz Phase Is Its Mass, It Pins Dynamically, and It Fills About a Quarter of the Core

**C. P. Zimmerman**
*Briar Creek Tech · Charlotte, NC · carl@briarcreektech.com*

*Version 2026-09-01 · DRAFT, not yet deposited. Companion to Zenodo [10.5281/zenodo.20779562](https://doi.org/10.5281/zenodo.20779562), two of whose statements this paper corrects (§7).*

---

## Abstract

Relativistic MOND completions leave a factor-≈2 missing-mass residual in galaxy-cluster cores. In Aether–Scalar–Tensor (AeST) theory the static weak-field equation for the potential is a modified Helmholtz equation, ∇·[M(x)∇Φ] + μ²Φ = 4πGρ_b (Durakovic & Skordis 2024), whose homogeneous solutions oscillate; the boundary constant, "the oscillation phase", sets an effective core mass and has been treated as a free parameter. A companion paper (Zenodo 20779562) found the resulting potential-depth lever real and galaxy-safe but descriptive, and named a 3-D N-body phase-pinning calculation as the single un-closed branch; three earlier dynamical solves found no pin because a free Klein–Gordon mode at ω = μc is undamped. We show, from the action, that the phase belongs to a different branch. With K(Q) = K₂(Q−Q₀)² and the k-essence identities p = L, ρ = QL′ − L, the AeST Q-sector dust obeys **p_d = (2πG/μ²)ρ_d²**, a γ = 2 (Lane–Emden n = 1) polytrope, with c_s² = 4πGρ_d/μ² = 2w, and in a static well, where Q = (1−Ψ)Q₀, **c_s² = |Ψ|c²** and ρ_d = −μ²Ψ/(4πG), exactly the Durakovic–Skordis phantom. Hydrostatic equilibrium of this polytrope *is* the Helmholtz equation, and the free constant is the polytrope's Bernoulli constant, i.e. its captured mass; the n = 1 radius π/μ is mass-independent, which is the whole freedom. The Klein–Gordon equation the earlier solves integrated has a Yukawa static limit and is the gapped branch. Because sign(ρ_d) = sign(c_s²), any static branch carrying dust on a potential hill has a gradient instability growing at |c_s|k — 4.4 e-folds per Hubble time already at k = μ for |Ψ| = 10⁻⁶ — so every node-bearing branch is excluded; all ten branches of the matched cluster boundary-value problem carry one. The physical configuration is the unique positive polytrope with a free surface inside π/μ, and a one-dimensional Lagrangian γ = 2 hydrodynamic solve of dust falling into the growing MOND well of a 10¹⁵ M☉ cluster reaches it (force residual 1%, Mach 0.10 residual motions, core mass ratio 1.00 to the static solution) while a ±50% free-mode admixture in the initial conditions changes the core mass by ≤ 3%: **the phase pins.** With the captured mass set to the cosmic dust share inside R500, the core (< 420 kpc) receives 2.3–3.4 × 10¹³ M☉, **23–33% of the 10¹⁴ M☉ residual** across both a₀ footings and both interpolating kernels, galaxy-safe by geometry (a Milky-Way share leaves 9 × 10⁷ M☉ inside 20 kpc). The same configuration gives η(R500) = 2.57 on the framework's kernel, within 10% of the raw eRASS1 value 2.33 with zero tuning, but overshoots the weak-lensing-corrected 1.7 on every kernel while undershooting the core: only 3% of the captured dust sits inside 420 kpc, because the profile ρ_d ∝ C − Ψ cannot be more concentrated than the potential. The shape, not the amount, is the binding limit. The lever scales as (μR)² and exists only at AeST's phenomenological μ⁻¹ ≈ 1 Mpc. Two statements of the companion paper are withdrawn: the dust is not pressureless inside wells, so the density-ordering veto does not apply, and no N-body run is needed to settle the phase. The cluster core gap remains at least 65% open. All results are reproduced by committed scripts; a₀, κ and the dust amplitude I₀ are inputs, never derived.

---

## 1. The question, and what was believed about it

MOND reproduces galaxy rotation curves with one acceleration scale but leaves a missing-mass discrepancy of a factor ≈ 2 in cluster cores (Sanders 1999, 2003), shared by its relativistic completions. Within the de Sitter–MOND framework (a₀ = c²√(Λ/32π) = 9.36 × 10⁻¹¹ m s⁻², with 1.13 × 10⁻¹⁰ on the alternative footing) the relativistic host is AeST (Skordis & Złośnik 2021), whose dark sector is the shift-symmetric scalar's temporal "Q-mode", a ghost-condensate-type excitation with cosmological density ∝ a⁻³.

In the static weak-field limit AeST reduces to a single equation for the potential (Verwayen, Skordis & Bœhm 2024; Durakovic & Skordis 2024, hereafter VSB24, DS24):

  (1/r²) d/dr[r² M(x) Φ′] + μ²Φ = 4πG ρ_b(r),  x = |Φ′|/a₀,  M(x) = (√(1+4x) − 1)/(√(1+4x) + 1),

where the +μ²Φ term is the scalar's mass term. Its sign makes the operator Helmholtz: the homogeneous solutions are [C₁ cos(μr) + C₂ sin(μr)]/r, and the absolute level of Φ is physical, acting as a phantom source ρ_ph = −μ²Φ/(4πG). VSB24 and DS24 treat the boundary constant as a free parameter; DS24 note that the cluster radial-acceleration relation can be enhanced or, further out, depressed "as if there is a negative mass density".

The companion paper (Zenodo 20779562) solved this equation on real cluster baryon profiles and found the lever real and large — up to 28–100% of the core residual — and galaxy- and Cassini-safe, but descriptive: the closure is set by the oscillation phase, which required a per-cluster tune, and it named "whether a full 3-D cosmological AeST N-body calculation dynamically pins the oscillation phase" as the single un-closed branch. Three subsequent dynamical solves (a scalar-only 1+1-D spherical collapse, a run adding self-consistency, the vector sector and violent relaxation, and a reduced 3-D prototype) found no pin: they evolved

  χ_tt − c_s²∇²χ + (μc)²χ = S,

whose free mode at ω = μc is conservative and undamped, so the late-time phase tracks the initial phase one-to-one.

This paper shows that the phase does not live in that mode.

## 2. The dust branch, from the action

### 2.1 Equation of state

Write the AeST scalar's temporal sector as L_Q = −F(0,Q)/(16πG̃) = K(Q)/(8πG̃) with K(Q) = K₂(Q−Q₀)² near the condensate minimum (Skordis & Złośnik 2021 write K = −2Λ + K₂(Q−Q₀)² + …; the v9 completion of the framework uses a DBI form with the same quadratic term). For a shift-symmetric scalar whose gradient is timelike, the standard k-essence identities give the fluid pressure and energy density as p = L and ρ = Q ∂L/∂Q − L. With u ≡ Q − Q₀:

  p = K₂u²/(8πG̃),  ρ = (2K₂Q₀u + K₂u²)/(8πG̃),  c_s² = K′/(QK″) = u/(Q₀ + u),  w = p/ρ = u/(2Q₀ + u).

At leading order c_s² = 2w, which is Skordis & Złośnik's adiabatic sound speed c_ad² = 2w₀/a³. Eliminating u at leading order and using the published quasi-static constants μ² = 2K₂Q₀²/(2−K_B) and G̃ = (1 − K_B/2)G,

  **p_d = (2πG/μ²) ρ_d²,  c_s² = dp_d/dρ_d = 4πG ρ_d/μ².**   (1)

The Q-sector dust is a polytrope of index γ = 2 (Lane–Emden n = 1). Its sound speed vanishes only at the cosmological density and grows linearly with the local dust density.

### 2.2 The static well

In the quasi-static limit Q = (1 − Ψ)Q₀ (the lapse redshifts the condensate's clock), so u = −Q₀Ψ and

  c_s² = −Ψ/(1 − Ψ) ≈ |Ψ| c²,  ρ_d = −μ²Ψ/(4πG).   (2)

The second expression is exactly DS24's phantom, recovered from the action with the correct G. The first says the dust inside any potential well is not cold: its pressure equals the potential depth, ≈ (1000 km s⁻¹)² in a cluster, ≈ (200 km s⁻¹)² in a galaxy.

### 2.3 Hydrostatics is the Helmholtz equation

Hydrostatic equilibrium of the polytrope (1) in a potential Ψ, ∇p_d = −ρ_d∇Ψ, is solved by

  ρ_d = μ²(C − Ψ)/(4πG),   (3)

with one free constant C, the Bernoulli constant. Substituting into Poisson's equation gives ∇²Ψ + μ²(Ψ − C) = 4πGρ_b: the DS24 equation, with the "oscillation phase" identified as C. For a self-gravitating polytrope of index n = 1 the Lane–Emden scale is α² = 2K_p/(4πG) = 1/μ², so the radius is π/μ for any mass; the polytrope holds any mass, which is why the static boundary-value problem cannot fix C. The DBI K(Q) of the framework's v9 action has the same quadratic term, so (1)–(3) transfer. All of §2 is verified symbolically (checks A1–A9 of the committed script).

### 2.4 Which branch the earlier solves evolved

The static limit of χ_tt − c_s²∇²χ + (μc)²χ = S is −c_s²∇²χ + μ²c²χ = S, a Yukawa operator: e^{−(μc/c_s)r}/r solves it and sin(μr)/r does not (check B1). It is the gapped scalar branch of Skordis & Złośnik (2022), not the dust branch whose static limit is Helmholtz. The undamped free mode at ω = μc is real physics but carries none of the freedom in (3).

## 3. Positivity pins the branch

From (1)–(2), sign(ρ_d) = sign(u) = sign(c_s²). A static solution that places dust on a potential hill (Ψ > C) has c_s² < 0 there: a gradient instability with growth rate |c_s|k, unbounded in k until the higher-derivative or DBI structure intervenes. At k = μ and |Ψ| = 10⁻⁶ (10⁻⁵) the rate is 9.7 × 10⁻¹⁸ s⁻¹ (3.1 × 10⁻¹⁷ s⁻¹), 4.4 (14) e-folds per Hubble time. Such a configuration is not a dynamical end state. This is the quantitative form of the expectation stated by Mistele, McGaugh & Hossenfelder (2023, §3), who note that the AeST oscillatory regime carries negative energy density, that condensates with negative energy density are expected to be unstable, and who truncate their solutions where the condensate density first reaches zero; it is also the ghost-condensate stability condition of Arkani-Hamed et al. (2004), P′ ≥ 0.

The admissible static configurations are therefore those with ρ_d ≥ 0 everywhere: the polytrope (3) inside a free surface R_s where C = Ψ(R_s), pure MOND outside. In the cluster boundary-value problem of the companion paper, the potential is matched at the turnaround radius r_ta = 8.5 Mpc, where μr_ta = 8.5 rad exceeds π: every branch that reaches the cosmological boundary value must oscillate through a node. We re-marched the ten branches recorded there (five each for the two cosmological boundary values). All ten carry a region of negative dust: the three high-core branches (η(R500) = 3.9, 1.7, 0.9; core phantom 4 × 10¹³, 1.7 × 10¹³, 1.1 × 10¹³ M☉) first go negative at 1.9, 1.4 and 1.1 Mpc, the two negative-core branches at 20–40 kpc (check C1). The phase menu of the static problem contains no physical member.

## 4. The physical family and what it delivers

### 4.1 Setup

We use the companion paper's solver and cluster: an A2029-type baryon profile (β-model gas, β = 0.67, r_c = 0.12 R500, f_gas = 0.13, plus a Hernquist BCG, f_* = 0.012) with M500 = 10¹⁵ M☉, R500 = 1.56 Mpc, marched in canonical-momentum form from r₀ = 20 kpc; μ⁻¹ = 1 Mpc (the CMB-pinned AeST value used by DS24 and by Blanchet & Skordis 2024); the DS24 kernel M(x) as primary and the framework's own a₀-line kernel, x = √(q² + q), as a sensitivity row; both a₀ footings. The dust term is active only while ρ_d > 0 and switches off permanently at the first zero (the free surface). The core residual target is 10¹⁴ M☉ inside 420 kpc (1.5 × 10¹⁴ as the harsher value). The cosmic dust share is f_d M_b with f_d = Ω_dm/Ω_b = 5.39: 7.6 × 10¹⁴ M☉ inside R500.

### 4.2 The one-parameter family

Sweeping the level C produces a positive-density family (check D1) whose surface radius saturates at 2.9–3.1 Mpc, below π/μ = 3.14 Mpc (D2), and whose core mass is monotone in the captured mass (D3):

| level −C [m² s⁻²] | R_s [Mpc] | M_dust,tot [M☉] | M_dust(<420 kpc) [M☉] | fraction of 10¹⁴ | η(R500) |
|---|---|---|---|---|---|
| 9.7 × 10¹¹ | 0.21 | 1.7 × 10¹¹ | 1.7 × 10¹¹ | 0.002 | 1.00 |
| 3.1 × 10¹² | 1.06 | 5.1 × 10¹³ | 1.0 × 10¹³ | 0.10 | 1.21 |
| 9.6 × 10¹² | 2.02 | 1.5 × 10¹⁵ | 4.7 × 10¹³ | 0.47 | 4.52 |
| 3.0 × 10¹³ | 2.48 | 1.0 × 10¹⁶ | 1.6 × 10¹⁴ | 1.62 | 13.8 |

(canonical footing, DS24 kernel). The phase is not free: it is the captured mass, and the captured mass is bounded by the cosmic share.

### 4.3 The pinned yield, both edges

At the cosmic share inside R500:

| footing / kernel | M_dust(<420 kpc) | % of 10¹⁴ | % of 1.5 × 10¹⁴ | η(R500) predicted |
|---|---|---|---|---|
| canonical / DS24 | 3.2 × 10¹³ | 32 | 21 | 3.17 |
| canonical / framework | 2.3 × 10¹³ | 23 | 15 | 2.57 |
| alternative / DS24 | 3.4 × 10¹³ | 33 | 22 | 3.14 |
| alternative / framework | 2.4 × 10¹³ | 24 | 16 | 2.56 |

The observed discrepancy at R500 for the eRASS1 sample on the framework's own kernel is η = 2.33 (raw hydrostatic) and ≈ 1.7 after weak-lensing mass calibration (Bulbul et al. 2024; Li et al. 2024). Two readings, both stated:

- For the framework: on its own kernel the budget-pinned configuration lands within 10% of the raw R500 value with zero tuning (check D9). This is the companion paper's "the abundance is not the problem" — the dark sector has the mass — now with the correct profile.
- Against: the same configuration overshoots the weak-lensing-corrected value on every kernel while undershooting the core (D8). Normalising the captured mass to the observed η(R500) instead of the budget leaves the core at 20–25% (raw) or 14–18% (WL) of 10¹⁴ M☉ (D10). The core's share of the captured dust is 3.1% (D6): with ρ_d ∝ C − Ψ and a logarithmic MOND potential, the dust profile is nearly flat, so mass scales as R³ and the 420-kpc core holds (0.42/1.5)³ of what R500 holds. **The shape, not the amount, is the binding limit.** No positive polytrope of any mass concentrates enough dust in the core without overshooting R500.

### 4.4 The μ fork

The lever scales as (μR)². At equal level, the core dust at μ⁻¹ = 22 Mpc (Blanchet & Skordis 2024, K_B = 0.5) is 2.2 × 10⁻³ of its 1-Mpc value, and at the framework's own Q-sector Helmholtz mass (μ⁻¹ = 4392 Mpc) it is 5 × 10⁻⁸ (D11). The result exists only at AeST's phenomenological μ⁻¹ ≈ 1 Mpc, which is a free parameter of the host theory, not an output of the framework.

## 5. Galaxy safety

The same rule applied to a Milky-Way-like galaxy (exponential disk, 6 × 10¹⁰ M☉, R_d = 3 kpc, plus a 10¹⁰ M☉ bulge) with its whole cosmic dust share of 3.8 × 10¹¹ M☉ captured: the polytrope's surface sits at 0.52 Mpc, the dust inside 20 kpc is 9 × 10⁷ M☉ against 6.9 × 10¹⁰ M☉ of baryons, and the acceleration at 10 kpc shifts by 10⁻⁴ dex (check E1). The protection is geometric, through μ²|Ψ|R³, and the ordering is by potential depth, as found in the companion item-B computation, not by density.

## 6. The time-dependent solve, in the correct form

The phase question is now a hydrodynamic one: does cold dust with the equation of state (1), falling into a forming cluster well, reach the hydrostatic polytrope, and does its final core mass remember the initial density pattern? We integrate a one-dimensional Lagrangian γ = 2 fluid (160 shells, artificial viscosity for compression, own gravity plus the baryonic MOND well grown over 3 Gyr, 12 Gyr total) for 3 × 10¹⁴ M☉ of dust initially uniform inside 4 Mpc with a mild outward flow.

- The end state is hydrostatic: median |∇p/ρ + ∇Ψ|/|∇Ψ| = 0.010 inside 2 Mpc, residual motions 200 km s⁻¹ = Mach 0.10 against the core sound speed of 2000 km s⁻¹ (F1).
- Its core mass, 2.03 × 10¹³ M☉, equals the static positive polytrope at the same captured mass, 2.02 × 10¹³ M☉ (F2).
- Adding a free-mode density pattern A sin(μr)/(μr) to the initial conditions with A = ±0.25, ±0.5 changes the final core mass by −3.2%, −1.3%, +1.0%, +2.0% (F3).

The phase is erased by the dynamics, not tracked. The earlier "no pin" was a true statement about the gapped branch and an irrelevant one for the cluster.

## 7. What this corrects, and what it does not do

**Withdrawn from the companion paper.** (i) Its §3 veto rested on "the Q-mode is sound-speed-zero sub-horizon, so its Jeans length vanishes and it clumps wherever density is highest". Equation (2) shows that c_s² → 0 holds only on the cosmic background; inside any well the dust's pressure equals the potential depth, and its equilibrium density tracks the potential, not the local baryon density. The density-ordering argument does not apply to this sector. (ii) Its statement that the single un-closed branch was a 3-D N-body phase-pinning run: the phase is settled in the dust branch by positivity and captured mass, without an N-body, and the earlier dynamical solves were integrating a different mode.

**Retained.** The companion paper's central conclusion stands and is sharpened: the dark sector has the cluster mass but cannot deploy it in the core. The reason is now geometric rather than a density veto.

**Not a closure.** Across footings, kernels and the two normalisations (budget or observed R500), the core receives 14–33% of its residual. The cluster core gap remains at least 65% open. This is a shared relativistic-MOND liability; nothing here is distinctive of the framework's coefficient.

**Caveats.** Spherical symmetry throughout (the vector sector is identically trivial in spherical symmetry, DS24 App. B). Baryons are prescribed, not co-evolved; the hydrodynamic run grows the well by hand. K(Q) is used at quadratic order; the DBI saturation is not reached at cluster depths (|Ψ| ~ 10⁻⁵). The "cosmic share inside R500" is one definition of the captured mass; the share inside the turnaround radius (4.5 × 10¹⁵ M☉) would overshoot R500 by a factor of 3–4 and is excluded by the same observation. μ⁻¹ = 1 Mpc is the host theory's phenomenological value.

## 8. Priority and attribution

The physics assembled here is largely known and is credited as follows. The quadratic shift-symmetric k-essence near its minimum behaves as dust plus a cosmological constant with c_s² ≪ 1 (Scherrer 2004; Guendelman, Nissimov & Pacheva 2016 give the explicit duality). A quadratic kinetic Lagrangian is the k-essence form of a γ = 2 polytrope (Chavanis 2021, eq. 89, in the Bose–Einstein-condensate context). The n = 1 polytrope's sin(kr)/kr profile with mass-independent radius is the Thomas–Fermi Bose–Einstein-condensate halo of Böhmer & Harko (2007). Mistele, McGaugh & Hossenfelder (2023, §3, Fig. 4) noted the negative energy density of the AeST oscillatory regime, its expected instability, the condensate analogy, and truncated their solutions at the first zero of the condensate density; the free-surface prescription of §3–4 has that priority. Blanchet & Skordis (2024, §5) identify the k < μ instability of the μ²(Q−1)² term as Jeans-type. The ghost-condensate stability condition is Arkani-Hamed et al. (2004). What we have not found stated elsewhere: the explicit identification of the DS24 Helmholtz equation as the Lane–Emden n = 1 hydrostatics of the AeST dust with the phase equal to its captured mass and c_s² = |Ψ| inside wells; and the cluster consequence (§3–6). DS24 and VSB24 treat the boundary constant as free and do not describe the scalar as a fluid; DS24's "isothermal" refers to the baryonic gas.

## 9. Two-sided summary

For the framework: the cluster lever is real, predictive with no per-cluster tune, galaxy-safe, and it reproduces the raw R500 discrepancy of a 10¹⁵ M☉ cluster to 10% on the framework's own kernel with zero free numbers. The dark sector's identity as a γ = 2 polytrope is a clean, checkable equation of state, and the phase-pinning question that was open since June is closed without an N-body.

Against: the pinned configuration overshoots the weak-lensing-corrected R500 value and fills only 23–33% of the core (14–25% when normalised to R500), because a profile ∝ C − Ψ cannot concentrate; the lever exists only at the host theory's phenomenological μ⁻¹ ≈ 1 Mpc and vanishes at the framework's own Q-sector mass; and two claims of the companion paper are withdrawn. The cluster core remains the framework's largest open liability.

## 10. Reproducibility

All numbers in this paper are printed by committed scripts that exit 0, each with checks that can fail and a mutation control that must fail:

- `qwen_claude_field_theory/closure_2026/cluster_phase_2026/itemC_phase_pinning_dynamics_2026.py` (27 checks; output `.out` committed; `MUTATE=1` flips the lapse relation and the Helmholtz sign and breaks A4/A5/C1/D3–D5) — §2–6.
- `itemA_reconstruct_lever_2026.py` (the DS24 solver, the branch menu, the μ fork) and `itemB_potential_depth_ordering_2026.py` (the |Φ| ordering, fixed-phase yields) in the same directory.
- `ITEM_C_PHASE_PINNING_VERDICT.md` in the same directory carries the priority ledger with sources.
- The companion paper's scripts are listed in Zenodo 20779562, §8.

Quarantine: a₀ = 9.36 × 10⁻¹¹ m s⁻² (canonical) and 1.13 × 10⁻¹⁰ (alternative), κ, and the dust amplitude I₀ are inputs. Nothing in this paper derives them.

## 11. References

- Arkani-Hamed N., Cheng H.-C., Luty M. A., Mukohyama S., 2004, JHEP 05, 074 (hep-th/0312099)
- Armendariz-Picon C., Lim E. A., 2005, JCAP 08, 007 (astro-ph/0505207)
- Blanchet L., Skordis C., 2024, JCAP 11, 040 (arXiv:2404.06584)
- Böhmer C. G., Harko T., 2007, JCAP 06, 025
- Bulbul E. et al., 2024, eRASS1 cluster catalogue (A&A)
- Chavanis P.-H., 2021, arXiv:2109.05963 (Astronomy 2022, 1, 126)
- Durakovic A., Skordis C., 2024, JCAP 04, 040 (arXiv:2312.00889) — DS24
- Guendelman E., Nissimov E., Pacheva S., 2016, EPJC 76, 90 (arXiv:1511.07071)
- Kelleher R., Lelli F., 2024, arXiv:2405.08557
- Li et al., 2024, weak-lensing mass calibration of eRASS1 clusters
- Mistele T., McGaugh S., Hossenfelder S., 2023, A&A 676, A100 (arXiv:2301.03499)
- Sanders R. H., 1999, ApJ 512, L23; 2003, MNRAS 342, 901
- Scherrer R. J., 2004, PRL 93, 011301 (astro-ph/0402316)
- Skordis C., Złośnik T., 2021, PRL 127, 161302 (arXiv:2007.00082); 2022, PRD 106, 104041 (arXiv:2109.13287)
- Verwayen P., Skordis C., Bœhm C., 2024, MNRAS 531, 272 (arXiv:2304.05134) — VSB24
- Zimmerman C. P., 2026, Zenodo 10.5281/zenodo.20779562 (the companion cluster no-go)
